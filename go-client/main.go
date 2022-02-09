package main

import (
	"fmt"
	"log"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"

	"github.com/gin-gonic/gin"
)

type request struct {
	KubeUser struct {
		Name string `json:"name"`
		User struct {
			AuthProvider struct {
				Name   string `json:"name"`
				Config struct {
					ClientID     string `json:"client-id"`
					IdpIssuerURL string `json:"idp-issuer-url"`
					IDToken      string `json:"id-token"`
					RefreshToken string `json:"refresh-token"`
					ClientSecret string `json:"client-secret"`
				} `json:"config"`
			} `json:"auth-provider"`
		} `json:"user"`
	} `json:"kube_user"`
	KubeCluster struct {
		Name    string `json:"name"`
		Cluster struct {
			CertificateAuthorityData string `json:"certificate-authority-data"`
			Server                   string `json:"server"`
		} `json:"cluster"`
	} `json:"kube_cluster"`
	KubeContext struct {
		Name    string `json:"name"`
		Context struct {
			Cluster string `json:"cluster"`
			User    string `json:"user"`
		} `json:"context"`
	} `json:"kube_context"`
	Context string `json:"context"`
}

func main() {
	// Get and validate the argument
	var url string
	if len(os.Args) == 2 {
		if isValidUrl(os.Args[1]) {
			url = os.Args[1]
		} else {
			fmt.Println("Argument is not a valid url")
			os.Exit(2)
		}
	} else {
		fmt.Println("Incorrect Number of Arguments Provided")
		os.Exit(2)
	}

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

	// Start webserver for callback
	//// Run background
	gin.SetMode(gin.ReleaseMode)
	router := gin.New()
	router.POST("/", callback)
	router.Run(":8080")
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

func callback(c *gin.Context) {
	var dirname string
	var filename string
	homedir, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	} else {
		dirname = filepath.Join(homedir, ".kue")
		filename = filepath.Join(dirname, "config")

		fmt.Println(filename)
		// test if exists
		if _, err := os.Stat(dirname); os.IsNotExist(err) {
			// dir does not exist so make dir
			os.Mkdir(dirname, os.ModePerm)
		} else if _, err := os.Stat(filename); os.IsNotExist(err) {
			// file does not exist
			// write to file function
			fmt.Println(filename) // debug
		} else {
			// file exists so read file
			file, err := os.Open(filename)
			if err != nil {
				log.Fatal(err)
				os.Exit(1)
			}
			fmt.Println(file) // debug
			// write to file function
		}
	}

	/*if _, err := os.Stat(dirname); os.IsNotExist(err) {
		// path/to/whatever does not exist
	}*/

	var request request
	c.BindJSON(&request)
	fmt.Println(string(request.KubeUser.Name))

	c.JSON(200, "Client Get Data")
	//os.Exit(0)
}

// https://dev.to/heroku/deploying-your-first-golang-webapp-11b3
// https://go.dev/doc/tutorial/web-service-gin
// https://www.sohamkamani.com/golang/how-to-build-a-web-application/
// https://stackoverflow.com/questions/42247978/go-gin-gonic-get-text-from-post-request
// https://chenyitian.gitbooks.io/gin-web-framework/content/docs/38.html

//// https://mholt.github.io/json-to-go/
