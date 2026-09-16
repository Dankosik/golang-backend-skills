package fixture

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestContractTenantDenial(t *testing.T) {
	records := map[string]Record{"b": {Tenant: "tenant-b", Body: "private-b"}}
	r := httptest.NewRequest(http.MethodGet, "/records/b", nil)
	r.Header.Set("X-Tenant", "tenant-b")
	w := httptest.NewRecorder()
	NewHandler("tenant-a", records).ServeHTTP(w, r)
	if w.Code != 403 {
		t.Errorf("denial status = %d", w.Code)
	}
	if strings.Contains(w.Body.String(), "private-b") {
		t.Error("protected data escaped")
	}
}
func TestContractTenantAccess(t *testing.T) {
	records := map[string]Record{"a": {Tenant: "tenant-a", Body: "public-to-a"}}
	for _, c := range []struct {
		path   string
		status int
		body   string
	}{
		{"/records/a", 200, "public-to-a"}, {"/records/missing", 404, ""},
	} {
		w := httptest.NewRecorder()
		NewHandler("tenant-a", records).ServeHTTP(w, httptest.NewRequest(http.MethodGet, c.path, nil))
		if w.Code != c.status {
			t.Errorf("%s: status = %d", c.path, w.Code)
		}
		if c.body != "" && w.Body.String() != c.body {
			t.Errorf("allowed body = %q", w.Body.String())
		}
	}
}
