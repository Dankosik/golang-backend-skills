package fixture

import (
	"errors"
	"io"
	"testing"
)

type countedCloser struct{ calls int }

func (c *countedCloser) Close() error { c.calls++; return nil }

func TestEvalPartialStartupCleanup(t *testing.T) {
	resource := &countedCloser{}
	failure := errors.New("second dependency unavailable")
	got, err := Start(func() (io.Closer, error) { return resource, nil }, func() error { return failure })
	if got != nil || !errors.Is(err, failure) || resource.calls != 1 {
		t.Fatalf("got resource=%v error=%v closes=%d; want nil, original error, one close", got, err, resource.calls)
	}
}

func TestEvalSuccessfulStartupOwnership(t *testing.T) {
	resource := &countedCloser{}
	got, err := Start(func() (io.Closer, error) { return resource, nil }, func() error { return nil })
	if err != nil || got != resource || resource.calls != 0 {
		t.Fatalf("successful startup must transfer the open resource to caller")
	}
	if err := got.Close(); err != nil || resource.calls != 1 {
		t.Fatal("caller could not close the resource once")
	}
}
