package fixture

import (
	"database/sql"
	"math"
	"testing"
)

func TestEvalNullableMapping(t *testing.T) {
	absent := Map(Row{Name: sql.NullString{String: "ignored"}, Count: sql.NullInt64{Int64: 9}})
	if absent.Name != nil || absent.Count != nil {
		t.Error("invalid database values must remain absent regardless of payload")
	}
	zero := Map(Row{Name: sql.NullString{Valid: true}, Count: sql.NullInt64{Valid: true}})
	if zero.Name == nil || *zero.Name != "" || zero.Count == nil || *zero.Count != 0 {
		t.Error("valid empty string and zero must not become absent")
	}
	large := Map(Row{Count: sql.NullInt64{Int64: math.MaxInt64, Valid: true}})
	if large.Count == nil || *large.Count != math.MaxInt64 {
		t.Error("int64 precision was lost")
	}
}
