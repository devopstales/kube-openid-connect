package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"

	"context"
	"net/http"
	"os/signal"
	"time"

	"github.com/gin-gonic/gin"
	pkgruntime "k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/tools/clientcmd"
	"sigs.k8s.io/yaml"

	clientcmdapi "k8s.io/client-go/tools/clientcmd/api"
	clientcmdlatest "k8s.io/client-go/tools/clientcmd/api/latest"
)

const (
	kubeConfigEnvName         = "KUBECONFIG"
	kubeConfigDefaultFilename = "~/.kube/config"
	AppVersion = "0.2"
)

type request struct {
	Context                  string `json:"context"`
	Server                   string `json:"server"`
	CertificateAuthorityData string `json:"certificate-authority-data"`
	ClientID                 string `json:"client-id"`
	IDToken                  string `json:"id-token"`
	RefreshToken             string `json:"refresh-token"`
	IdpIssuerURL             string `json:"idp-issuer-url"`
	ClientSecret             string `json:"client_secret"`
}

func main() {
	// Print version
	version := flag.Bool("v", false, "prints current app version")
	flag.Parse()
	if *version {
		fmt.Println(AppVersion)
		os.Exit(0)
	}
	// Get and validate the argument
	if len(os.Args) == 2 {
		if isValidUrl(os.Args[1]) {
			OpenInBrowser(os.Args[1])
		} else {
			fmt.Println("Argument is not a valid url")
			os.Exit(2)
		}
	} else {
		fmt.Println("Incorrect Number of Arguments Provided")
		os.Exit(2)
	}

	// Start webserver for callback
	gin.SetMode(gin.ReleaseMode)
	router := gin.New()
	router.POST("/", callback)
	//router.Run(":8080")
	////////////////////////////////////////

	srv := &http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	go func() {
		// service connections
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	quit := make(chan os.Signal)
	signal.Notify(quit, os.Interrupt)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server Shutdown:", err)
	}
}

func isValidUrl(toTest string) bool {
	_, err := url.ParseRequestURI(toTest)
	if err != nil {
		return false
	}

	u, err := url.Parse(toTest)
	if err != nil || u.Scheme == "" || u.Host == "" {
		return false
	}

	return true
}

func OpenInBrowser(url string) {
	// Open in browser
	var err error
	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", url).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = fmt.Errorf("unsupported platform")
	}
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
}

func callback(c *gin.Context) {
	var request request
	// Debug
	/*
		body, _ := ioutil.ReadAll(c.Request.Body)
		println(string(body))
	*/
	// Debug
	c.BindJSON(&request)
	// fmt.Println(string(request.Context)) // Debug

	// Read config
	var fileExist bool
	var kubeconfig string
	fileExist, kubeconfig = GetKubeConfig()

	if fileExist == true {
		configOverrides, _ := ioutil.TempFile("", "")
		defer os.Remove(configOverrides.Name())

		// Get config from request and write to file
		requestConfig, context := createValidTestConfig(request)
		clientcmd.WriteToFile(requestConfig, configOverrides.Name())

		// merge files
		loadingRules := clientcmd.ClientConfigLoadingRules{
			Precedence: []string{kubeconfig, configOverrides.Name()},
		}

		mergedConfig, err := loadingRules.Load()
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}
		json, err := pkgruntime.Encode(clientcmdlatest.Codec, mergedConfig)
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}
		output, err := yaml.JSONToYAML(json)
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}

		//fmt.Println(string(output)) // Debug
		// Write to file
		WriteToFile(string(output), context)
	} else {
		configOverrides, _ := ioutil.TempFile("", "")
		defer os.Remove(configOverrides.Name())

		// Get config from request and write to file
		requestConfig, context := createValidTestConfig(request)
		clientcmd.WriteToFile(requestConfig, configOverrides.Name())

		// merge file
		loadingRules := clientcmd.ClientConfigLoadingRules{
			Precedence: []string{configOverrides.Name()},
		}

		kubeConfig, err := loadingRules.Load()
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}
		json, err := pkgruntime.Encode(clientcmdlatest.Codec, kubeConfig)
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}
		output, err := yaml.JSONToYAML(json)
		if err != nil {
			fmt.Printf("Unexpected error: %v", err)
		}

		//fmt.Println(string(output)) // Debug
		// Write to file
		WriteToFile(string(output), context)
	}
	c.JSON(200, "Client Get Data")
	return
}

func GetKubeConfig() (bool, string) {
	var fileExist bool
	var kubeConfigFileName string

	ConfigFilename := os.Getenv(kubeConfigEnvName)
	if ConfigFilename == "" {
		homedir, err := os.UserHomeDir()
		if err != nil {
			log.Fatal(err)
			os.Exit(1)
		} else {
			var dirname string = filepath.Join(homedir, ".kube")
			var filename string = filepath.Join(dirname, "config")

			// test if filename exists
			if _, err := os.Stat(dirname); os.IsNotExist(err) {
				// dir does not exist so create it
				// fmt.Println("dir does not exist so create it") // Debug
				os.Mkdir(dirname, 0755)
				fileExist = false
			} else if _, err := os.Stat(filename); os.IsNotExist(err) {
				// file does not exist
				// fmt.Println("file does not exist") // Debug
				fileExist = false
			} else {
				// file exists
				// fmt.Println("file exist") // Debug
				fileExist = true
			}
			kubeConfigFileName = filename
		}
	} else {
		// test if kubeConfigEnvName exists
		if _, err := os.Stat(kubeConfigFileName); os.IsNotExist(err) {
			// file does not exist
			fileExist = false
		} else {
			// file exists
			fileExist = true
		}
		kubeConfigFileName = ConfigFilename
	}
	return fileExist, kubeConfigFileName
}

func createValidTestConfig(request request) (clientcmdapi.Config, string) {
	/*
		const (
			// demo data for test
			context          = "cl04"
			k8s_server_url   = "https://anything.com:8080"
			client_id        = "dashboard-proxy"
			client_secret    = "df4c4725-98c9"
			id_token         = "eyJhbGciOiJSUzI1NiIs..."
			oauth_server_uri = "https://sso.anything.com/auth/realms/someting"
			refresh_token    = "eyJhbGciOiJIUzI1NiIsInR5cCI___"
			CA               = "-----BEGIN CERTIFICATE-----MIIELTCCApWgAwIBAgIRAODbJ0M+pR7t/0VsFRfGR5UwDQYJKoZIhvcNAQELBQAwLzEsfqPPVSmiR8W2eYJ8JQ=-----END CERTIFICATE-----"
		)
	*/

	var (
		kubeConfig = clientcmdapi.Config{
			AuthInfos: map[string]*clientcmdapi.AuthInfo{
				request.Context: {
					AuthProvider: &clientcmdapi.AuthProviderConfig{
						Name: "oidc",
						Config: map[string]string{
							"client-id":      request.ClientID,
							"client-secret":  request.ClientSecret,
							"id-token":       request.IDToken,
							"idp-issuer-url": request.IdpIssuerURL,
							"refresh-token":  request.RefreshToken,
						},
					},
				},
			},
			Clusters: map[string]*clientcmdapi.Cluster{
				request.Context: {
					Server:                   request.Server,
					CertificateAuthorityData: []byte(request.CertificateAuthorityData),
				},
			},
			Contexts: map[string]*clientcmdapi.Context{
				request.Context: {
					AuthInfo: request.Context,
					Cluster:  request.Context,
				},
			},
		}
	)

	return kubeConfig, request.Context
}

func WriteToFile(content string, context string) {
	homedir, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
	var dirname string = filepath.Join(homedir, ".kube")
	var filename string = filepath.Join(dirname, "config")

	f, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)

	}
	defer f.Close()

	_, err2 := f.WriteString(content)

	if err2 != nil {
		log.Fatal(err2)
	}
	fmt.Printf("Configfile created with config for %s to %s\n", context, filename)
	fmt.Println("Happy Kubernetes interaction!")
	fmt.Println("(Press CTRL+C to quit)")
}
