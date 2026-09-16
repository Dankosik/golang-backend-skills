package fixture

import "errors"

var ErrRange = errors.New("invalid range")

func Clamp(value, min, max int) (int, error) {
	return value, nil
}
