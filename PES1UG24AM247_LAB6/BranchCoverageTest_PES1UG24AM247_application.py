
import pytest
from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


# 1. Invalid input branches
def test_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_credit_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


# 2. Empty and unapproved batches
def test_empty_batches():
    result = process_book_buybacks([], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_unapproved_batch():
    batches = [
        {
            "intake_approved": False,
            "format": "paperback",
            "books": [{"condition": "good"}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


# 3. All supported and unsupported formats
def test_all_book_formats():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"condition": "good"}]
        },
        {
            "intake_approved": True,
            "format": "audiobook",
            "books": [{"condition": "good"}]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "COMPLETED"
    assert result["total_payout"] == 63.0


# 4. Default format and empty books
def test_default_format_empty_books_with_credit():
    batches = [
        {
            "intake_approved": True,
            "payout_in_credit": True
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 5.0
    assert result["status"] == "COMPLETED"


# 5. Missing pages rejection
def test_missing_pages():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 2, "condition": "good"}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


# 6. Counterfeit textbook causes batch break
def test_counterfeit_textbook():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [
                {"counterfeit": True},
                {"condition": "mint"}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# 7. Counterfeit non-textbook
def test_counterfeit_hardcover():
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": [
                {"counterfeit": True},
                {"condition": "good"}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


# 8. All book conditions
def test_mint_poor_and_good_conditions():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"condition": "mint"},
                {"condition": "poor"},
                {"condition": "good"}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 21.2


# 9. Store credit bonus disabled and enabled
def test_store_credit_bonus():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": True,
            "books": [{"condition": "good"}]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 13.0


# 10. Audit rejection after more than four rejected books
def test_audit_rejected():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 1},
                {"missing_pages": 2},
                {"missing_pages": 3},
                {"missing_pages": 4},
                {"missing_pages": 5}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "AUDIT_REJECTED"


# 11. Exactly four rejected books should not trigger audit
def test_four_rejections_not_audit():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 1},
                {"missing_pages": 2},
                {"missing_pages": 3},
                {"missing_pages": 4},
                {"condition": "good"}
            ]
        }
    ]

    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "COMPLETED"
    assert result["total_payout"] == 8.0


# 12. Scanner with no data
def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


# 13. Scanner with empty device readings
def test_scanner_empty_device_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"


# 14. Scanner with normal readings
def test_scanner_calibrated():
    assert inspect_scanner_calibration([
        [1, 2, 3, 4],
        [6, 2, 3]
    ]) == "CALIBRATED"


# 15. One high error followed by a normal reading resets streak
def test_scanner_streak_reset():
    assert inspect_scanner_calibration([
        [6, 2, 7, 1]
    ]) == "CALIBRATED"


# 16. Two consecutive high errors require recalibration
def test_scanner_recalibration():
    assert inspect_scanner_calibration([
        [1, 6, 7, 2]
    ]) == "RECALIBRATE"
