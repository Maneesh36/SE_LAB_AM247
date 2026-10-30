
import pytest
from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


def test_invalid_batches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_store_credit_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -5.0)


def test_buyback_all_book_formats_and_conditions():
    batches = [
        # Unapproved batch
        {
            "intake_approved": False,
            "format": "textbook",
            "books": [{"condition": "good"}]
        },

        # Textbook: missing pages and counterfeit
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [
                {"missing_pages": 2, "condition": "good"},
                {"counterfeit": True, "condition": "mint"}
            ]
        },

        # Hardcover: mint, poor, good and counterfeit
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": [
                {"condition": "mint"},
                {"condition": "poor"},
                {"condition": "good"},
                {"counterfeit": True}
            ],
            "payout_in_credit": False
        },

        # Paperback: normal book
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"condition": "good"}]
        },

        # Default format and default empty books list
        {
            "intake_approved": True,
            "payout_in_credit": True
        },

        # Unsupported book format
        {
            "intake_approved": True,
            "format": "audiobook",
            "books": [{"condition": "good"}]
        }
    ]

    result = process_book_buybacks(batches, 5.0)

    assert result["total_payout"] > 0
    assert result["status"] == "COMPLETED"


def test_textbook_counterfeit_rejection():
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


def test_audit_rejection():
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

    assert result["total_payout"] == 0.0
    assert result["status"] == "AUDIT_REJECTED"


def test_zero_credit_for_empty_batches():
    result = process_book_buybacks([], 5.0)

    assert result == {
        "total_payout": 0.0,
        "status": "ZERO_CREDIT"
    }


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_calibrated():
    scanner_matrix = [
        [1, 2, 3, 4],
        [6, 2, 6]
    ]

    assert inspect_scanner_calibration(scanner_matrix) == "CALIBRATED"


def test_scanner_recalibration():
    scanner_matrix = [
        [1, 6, 7, 2]
    ]

    assert inspect_scanner_calibration(scanner_matrix) == "RECALIBRATE"
