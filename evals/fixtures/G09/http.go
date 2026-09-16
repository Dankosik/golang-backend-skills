package fixture

import (
	"fmt"
	"net/http"
)

func Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/error", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, `{"error":"%s"}`, r.URL.Query().Get("message"))
	})
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-App", "fixture")
		mux.ServeHTTP(w, r)
	})
}
