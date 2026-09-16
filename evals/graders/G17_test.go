package fixture

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestEvalTenantDenialProtectsEffect(t *testing.T) {
	item := &Item{Tenant: "b", Value: "original"}
	request := httptest.NewRequest(http.MethodPost, "/?id=record&tenant=b", nil)
	request.Header.Set("Authorization", "Bearer fixture-a")
	recorder := httptest.NewRecorder()
	Routes(map[string]*Item{"record": item}).ServeHTTP(recorder, request)
	if recorder.Code != http.StatusForbidden || item.Value != "original" {
		t.Fatalf("cross-tenant request: status=%d value=%q", recorder.Code, item.Value)
	}
}

func TestEvalTenantIntendedAccess(t *testing.T) {
	item := &Item{Tenant: "b", Value: "original"}
	request := httptest.NewRequest(http.MethodPost, "/?id=record", nil)
	request.Header.Set("Authorization", "Bearer fixture-b")
	recorder := httptest.NewRecorder()
	Routes(map[string]*Item{"record": item}).ServeHTTP(recorder, request)
	if recorder.Code != http.StatusNoContent || item.Value != "updated" {
		t.Fatalf("legitimate request: status=%d value=%q", recorder.Code, item.Value)
	}
}

func TestEvalUnauthenticatedRequest(t *testing.T) {
	item := &Item{Tenant: "b", Value: "original"}
	recorder := httptest.NewRecorder()
	Routes(map[string]*Item{"record": item}).ServeHTTP(recorder, httptest.NewRequest(http.MethodPost, "/?id=record&tenant=b", nil))
	if recorder.Code != http.StatusUnauthorized || item.Value != "original" {
		t.Fatal("unauthenticated request reached the protected effect")
	}
}
