package fixture

import (
	"database/sql"
	"testing"
)

func TestContractNull(t *testing.T) {
	if got := Convert(sql.NullInt64{Int64: 123, Valid: false}); got != nil {
		t.Errorf("null became %d", *got)
	}
}
func TestContractExactValue(t *testing.T) {
	for _, want := range []int64{0, -1, 9007199254740993, 9223372036854775807, -9223372036854775808} {
		value := sql.NullInt64{Int64: want, Valid: true}
		got := Convert(value)
		if got == nil || *got != want {
			t.Fatalf("lost value %d: %v", want, got)
		}
		*got = 42
		if value.Int64 != want {
			t.Fatal("mutated input")
		}
	}
}
