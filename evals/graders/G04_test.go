package fixture

import (
	"context"
	"errors"
	"testing"
	"time"
)

func TestEvalBlockedSendTerminates(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	out := make(chan int)
	started, stopped := make(chan struct{}), make(chan struct{})
	returned := make(chan error, 1)
	go func() { returned <- Run(ctx, out, started, stopped) }()
	select {
	case <-started:
	case <-time.After(time.Second):
		t.Fatal("worker did not start")
	}
	cancel()
	select {
	case err := <-returned:
		if !errors.Is(err, context.Canceled) {
			t.Errorf("want cancellation, got %v", err)
		}
		select {
		case <-stopped:
		default:
			t.Error("Run returned before owned work stopped")
		}
	case <-time.After(time.Second):
		t.Error("cancellation did not release the blocked send and join worker")
		// Release the seeded defect and join even on the failing path.
		select {
		case <-out:
		case <-time.After(time.Second):
			t.Fatal("cannot release worker")
		}
		select {
		case <-returned:
		case <-time.After(time.Second):
			t.Fatal("worker failed to join after release")
		}
	}
}
