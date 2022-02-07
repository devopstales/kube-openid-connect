package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"runtime"

	"github.com/gin-gonic/gin"
)

func main() {
	url := os.Args[1]

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
	}

	r := gin.Default()

	r.POST("/", callback)

	r.Run(":8080")
}

func callback(c *gin.Context) {

}

// https://dev.to/heroku/deploying-your-first-golang-webapp-11b3
// https://go.dev/doc/tutorial/web-service-gin
// https://www.sohamkamani.com/golang/how-to-build-a-web-application/
// https://stackoverflow.com/questions/42247978/go-gin-gonic-get-text-from-post-request
