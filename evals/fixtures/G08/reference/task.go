package fixture

type Resource interface{ Close() error }

func Build(first, second func() (Resource, error)) ([]Resource, error) {
	a, err := first()
	if err != nil {
		return nil, err
	}
	b, err := second()
	if err != nil {
		_ = a.Close()
		return nil, err
	}
	return []Resource{a, b}, nil
}
