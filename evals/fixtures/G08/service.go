package fixture

import "io"

func Start(open func() (io.Closer, error), connect func() error) (io.Closer, error) {
	resource, err := open()
	if err != nil {
		return nil, err
	}
	if err := connect(); err != nil {
		return nil, err
	}
	return resource, nil
}
