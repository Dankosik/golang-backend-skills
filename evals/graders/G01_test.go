package fixture

import (
	"errors"
	"testing"
)

func TestEvalClampBoundaries(t *testing.T) {
	cases := []struct{ value, minimum, maximum, want int }{
		{-3, -2, 5, -2}, {-2, -2, 5, -2}, {0, -2, 5, 0},
		{5, -2, 5, 5}, {6, -2, 5, 5}, {100, 4, 4, 4},
	}
	for _, tc := range cases {
		got, err := Clamp(tc.value, tc.minimum, tc.maximum)
		if err != nil || got != tc.want {
			t.Errorf("Clamp(%d, %d, %d) = %d, %v; want %d, nil", tc.value, tc.minimum, tc.maximum, got, err, tc.want)
		}
	}
}

func TestEvalInvalidRangeIdentity(t *testing.T) {
	_, err := Clamp(0, 5, -2)
	if !errors.Is(err, ErrInvalidRange) {
		t.Fatalf("invalid range must preserve ErrInvalidRange identity; got %v", err)
	}
}
