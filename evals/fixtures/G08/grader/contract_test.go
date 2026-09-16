package fixture

import (
	"errors"
	"testing"
)

type observedResource struct{ closes int }

func (r *observedResource) Close() error {
	r.closes++
	return errors.New("cleanup error")
}

func TestContractPartialStartup(t *testing.T) {
	a := &observedResource{}
	failure := errors.New("second constructor failed")
	resources, err := Build(func() (Resource, error) { return a, nil },
		func() (Resource, error) { return nil, failure })
	if !errors.Is(err, failure) {
		t.Errorf("original failure lost: %v", err)
	}
	if resources != nil {
		t.Error("failed startup returned resources")
	}
	if a.closes != 1 {
		t.Errorf("first resource closed %d times", a.closes)
	}
}
func TestContractSuccessfulStartup(t *testing.T) {
	a, b := &observedResource{}, &observedResource{}
	resources, err := Build(func() (Resource, error) { return a, nil },
		func() (Resource, error) { return b, nil })
	if err != nil || len(resources) != 2 {
		t.Fatalf("startup = %v,%v", resources, err)
	}
	if resources[0] != a || resources[1] != b {
		t.Error("resource identity/order changed")
	}
	if a.closes != 0 || b.closes != 0 {
		t.Error("closed a successful resource")
	}
	for _, resource := range resources {
		_ = resource.Close()
	}
}
func TestContractFirstFailure(t *testing.T) {
	failure := errors.New("first constructor failed")
	called := false
	resources, err := Build(func() (Resource, error) { return nil, failure },
		func() (Resource, error) { called = true; return &observedResource{}, nil })
	if !errors.Is(err, failure) || resources != nil || called {
		t.Errorf("first failure = %v,%v,second called %v", resources, err, called)
	}
}
