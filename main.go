package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"

	"database/sql"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

type Email struct {
	ID   int
	Body string
}

func getRandomEmail(db *sql.DB) *Email {
	var id int
	var body string

	err := db.QueryRow(`
		SELECT id, Body
		FROM enron_tags.enron
		WHERE Tag IS NULL
		ORDER BY RAND()
		LIMIT 1`).Scan(&id, &body)

	switch {
	case err == sql.ErrNoRows:
		log.Printf("No available email")
	case err != nil:
		log.Fatal(err)
	default:
		return &Email{id, body}
	}

	return &Email{0, "No email available"}
}

func setTag(db *sql.DB, emailID, tag string) {
	err := db.QueryRow(`
		UPDATE enron_tags.enron
		SET Tag = ?
		WHERE ID = ?`, tag, emailID).Scan()

	if err != nil {
		log.Println(err)
	}

}

func main() {
	db, err := sql.Open("mysql", "enron_tagger:CompilersProject@tcp(enron.c9hkwqr7bv7z.us-east-1.rds.amazonaws.com:3306)/enron_tags")
	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	tmpl := template.Must(template.ParseFiles("layout.html"))

	router := mux.NewRouter()

	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		email := getRandomEmail(db)
		tmpl.Execute(w, email)
	}).Methods("GET")

	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Received")
		params, _ := ioutil.ReadAll(r.Body)
		values, _ := url.ParseQuery(string(params))

		id := values["id"][0]
		tag := values["tag"][0]
		setTag(db, id, tag)
	}).Methods("POST")

	http.ListenAndServe(":8080", router)
}
