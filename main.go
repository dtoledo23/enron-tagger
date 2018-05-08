package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"

	"database/sql"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

type Email struct {
	ID       int
	Body     string
	Progress string
}

func getRandomEmail(db *sql.DB) *Email {
	var id int
	var body string
	var progress float64

	err := db.QueryRow(`
		SELECT id, body, progress()
		FROM email_tags
		WHERE tag IS NULL
		ORDER BY RANDOM()
		LIMIT 1`).Scan(&id, &body, &progress)

	pro := fmt.Sprintf("%f", progress*100)

	switch {
	case err == sql.ErrNoRows:
		log.Printf("No available email")
	case err != nil:
		log.Fatal(err)
	default:
		return &Email{id, body, pro}
	}

	return &Email{0, "No email available", ""}
}

func setTag(db *sql.DB, emailID, tag string) {
	_, err := db.Exec(`
		UPDATE email_tags
		SET tag = $1
		WHERE id = $2`, tag, emailID)

	if err != nil {
		log.Println(err)
	}

}

func main() {
	db, err := sql.Open("postgres", "postgres://postgres@localhost:5432/enron_corpora?sslmode=disable")
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
