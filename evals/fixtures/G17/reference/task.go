package fixture

import (
	"fmt"
	"net/http"
	"strings"
)

type Record struct{ Tenant, Body string }

func NewHandler(tenant string, records map[string]Record) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/records/", func(w http.ResponseWriter, r *http.Request) {
		id := strings.TrimPrefix(r.URL.Path, "/records/")
		record, ok := records[id]
		if !ok {
			http.NotFound(w, r)
			return
		}
		if record.Tenant != tenant {
			http.Error(w, "forbidden", http.StatusForbidden)
			return
		}
		fmt.Fprint(w, record.Body)
	})
	return mux
}
