package fixture

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestContractMountedError(t *testing.T) {
	w := httptest.NewRecorder()
	NewHandler().ServeHTTP(w, httptest.NewRequest(http.MethodGet, "/item", nil))
	response := w.Result()
	defer response.Body.Close()
	if response.StatusCode != 400 {
		t.Errorf("status = %d", response.StatusCode)
	}
	if response.Header.Get("Content-Type") != "application/json" {
		t.Errorf("content type = %q", response.Header.Get("Content-Type"))
	}
	if response.Header.Get("X-Service") != "fixture" {
		t.Error("mounted middleware missing")
	}
	var body map[string]string
	if err := json.Unmarshal(w.Body.Bytes(), &body); err != nil {
		t.Fatal(err)
	}
	if len(body) != 1 || body["error"] != "invalid" {
		t.Errorf("body = %#v", body)
	}
}
func TestContractUnknownRoute(t *testing.T) {
	w := httptest.NewRecorder()
	NewHandler().ServeHTTP(w, httptest.NewRequest(http.MethodGet, "/missing", nil))
	if w.Code != 404 || w.Header().Get("X-Service") != "fixture" {
		t.Errorf("fallback = %d,%v", w.Code, w.Header())
	}
}
