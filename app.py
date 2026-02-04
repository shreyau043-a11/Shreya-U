import json
from typing import Any, Dict

import streamlit as st

from classifer import classify_po


st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("PO L1–L2–L3 Classifier")
st.caption("Paste a PO description and optionally a supplier to classify.")


def parse_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        return json.loads(result)
    raise ValueError("Unsupported model response type.")


if "history" not in st.session_state:
    st.session_state.history = []

with st.form("classifier_form", clear_on_submit=False):
    po_description = st.text_area("PO Description", height=140)
    supplier = st.text_input("Supplier (optional)")
    show_raw = st.checkbox("Show raw response", value=False)
    submit = st.form_submit_button("Classify")

if submit:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            try:
                result = classify_po(po_description.strip(), supplier.strip())
                parsed = parse_result(result)
                st.success("Classification complete.")
                st.json(parsed)

                st.session_state.history.insert(
                    0,
                    {
                        "po_description": po_description.strip(),
                        "supplier": supplier.strip(),
                        "result": parsed,
                    },
                )
            except Exception as exc:
                st.error("Invalid model response")
                if show_raw:
                    st.text(str(exc))
                    st.text(result if "result" in locals() else "No response returned.")

st.divider()
st.subheader("Recent Classifications")

if st.session_state.history:
    for item in st.session_state.history[:5]:
        st.write(f"PO: {item['po_description']}")
        if item["supplier"]:
            st.write(f"Supplier: {item['supplier']}")
        st.json(item["result"])
        st.divider()
else:
    st.info("No classifications yet.")

if st.button("Clear history"):
    st.session_state.history = []





