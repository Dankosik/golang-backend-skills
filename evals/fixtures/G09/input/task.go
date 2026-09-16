package fixture

import "net/http"

func NewHandler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/item", func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "invalid", http.StatusBadRequest)
	})
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Service", "fixture")
		mux.ServeHTTP(w, r)
	})
}
