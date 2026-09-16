package fixture

import "context"

// The caller supplies channels to observe the worker's lifetime.
func Run(ctx context.Context, out chan<- int, started, stopped chan struct{}) error {
	done := make(chan struct{})
	go func() {
		defer close(done)
		defer close(stopped)
		close(started)
		out <- 1
	}()
	<-ctx.Done()
	<-done
	return ctx.Err()
}
