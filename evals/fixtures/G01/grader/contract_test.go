package fixture

import (
	"errors"
	"testing"
)

func TestContractClamp(t *testing.T) {
	cases := []struct{ value, min, max, want int }{
		{-9, -3, 4, -3}, {8, -3, 4, 4}, {2, -3, 4, 2},
		{-3, -3, 4, -3}, {4, -3, 4, 4}, {99, 7, 7, 7},
	}
	for _, c := range cases {
		got, err := Clamp(c.value, c.min, c.max)
		if err != nil || got != c.want {
			t.Errorf("Clamp(%d,%d,%d) = %d,%v; want %d,nil", c.value, c.min, c.max, got, err, c.want)
		}
	}
}
func TestContractRangeError(t *testing.T) {
	for _, v := range []int{-99, 0, 99} {
		_, err := Clamp(v, 4, -3)
		if !errors.Is(err, ErrRange) {
			t.Errorf("invalid range: got %v; want ErrRange", err)
		}
	}
}
