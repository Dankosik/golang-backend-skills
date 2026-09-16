package fixture

import "errors"

var ErrInvalidRange = errors.New("invalid range")

func Clamp(value, minimum, maximum int) (int, error) {
	if minimum > maximum {
		return 0, errors.New("invalid range")
	}
	if value < minimum {
		return minimum, nil
	}
	if value > maximum {
		return maximum, nil
	}
	return value, nil
}
