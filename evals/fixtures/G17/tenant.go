package fixture

import (
	"context"
	"net/http"
)

type tenantKey struct{}
type Item struct{ Tenant, Value string }

// Fixed tokens are a controlled authentication collaborator, not production crypto.
func Routes(items map[string]*Item) http.Handler {
	operation := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		item := items[r.URL.Query().Get("id")]
		if item == nil {
			http.NotFound(w, r)
			return
		}
		if item.Tenant != r.URL.Query().Get("tenant") {
			http.Error(w, "forbidden", http.StatusForbidden)
			return
		}
		item.Value = "updated"
		w.WriteHeader(http.StatusNoContent)
	})
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		tenant := map[string]string{"Bearer fixture-a": "a", "Bearer fixture-b": "b"}[r.Header.Get("Authorization")]
		if tenant == "" {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		operation.ServeHTTP(w, r.WithContext(context.WithValue(r.Context(), tenantKey{}, tenant)))
	})
}
