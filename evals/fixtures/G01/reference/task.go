package fixture

import "errors"

var ErrRange = errors.New("invalid range")

func Clamp(value, min, max int) (int, error) {
	if min > max {
		return 0, ErrRange
	}
	if value < min {
		return min, nil
	}
	if value > max {
		return max, nil
	}
	return value, nil
}
