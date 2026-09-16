package fixture

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"
)

func TestEvalMountedErrorContract(t *testing.T) {
	for _, message := range []string{"ordinary", "quote: \"", "line\nbreak", "backslash: \\"} {
		recorder := httptest.NewRecorder()
		request := httptest.NewRequest(http.MethodGet, "/error?message="+url.QueryEscape(message), nil)
		Routes().ServeHTTP(recorder, request)
		if recorder.Code != http.StatusBadRequest || recorder.Header().Get("Content-Type") != "application/json" || recorder.Header().Get("X-App") != "fixture" {
			t.Errorf("mounted status/header contract changed: %d %v", recorder.Code, recorder.Header())
		}
		var body map[string]string
		if err := json.Unmarshal(recorder.Body.Bytes(), &body); err != nil || len(body) != 1 || body["error"] != message {
			t.Errorf("error response must encode the original message: body=%q err=%v", recorder.Body.String(), err)
		}
	}
}
