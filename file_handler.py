"""
Basic File Handling - Streamlit App
Task 3

Reads a text file, finds/replaces words, and saves the result — either as
a downloadable file (works on any machine, recommended) or by writing
directly back to a file path on the server/local disk (only works if you
run this locally and the path is correct).

Run with:
    pip install streamlit
    streamlit run file_handler.py
"""

import streamlit as st
import os
import io

st.set_page_config(page_title="File Handler", page_icon="📄", layout="centered")

st.title("📄 Basic File Handler")
st.write("Read a text file, find and replace words, and save the changes.")

# ---------------------------------------------------------------------------
# Mode selection
# ---------------------------------------------------------------------------

mode = st.radio(
    "How do you want to load the file?",
    ["Upload a file", "Read from a local file path"],
    help=(
        "Upload works from any browser/machine. 'Local file path' only "
        "works if this app runs on the same machine as the file, and "
        "writes changes directly back to that same path on disk."
    ),
)

content = None
source_label = None
local_path = None

# ---------------------------------------------------------------------------
# Load content
# ---------------------------------------------------------------------------

if mode == "Upload a file":
    uploaded = st.file_uploader("Choose a .txt file", type=["txt", "csv", "log", "md"])
    if uploaded is not None:
        try:
            raw = uploaded.read()
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("latin-1")
                st.info("File wasn't UTF-8 — decoded as Latin-1 instead.")
            source_label = uploaded.name
        except Exception as e:
            st.error(f"Couldn't read the uploaded file: {e}")

else:
    local_path = st.text_input(
        "Full file path",
        placeholder=r"e.g. C:\Users\you\Documents\notes.txt  or  /home/user/notes.txt",
    )
    if local_path:
        if not os.path.exists(local_path):
            st.error(
                f"File not found at that path: {local_path}\n\n"
                "Common causes: wrong slashes for your OS, missing file "
                "extension, or running the app from a different working "
                "directory than you expect."
            )
        elif not os.path.isfile(local_path):
            st.error("That path exists but is a directory, not a file.")
        else:
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    content = f.read()
                source_label = local_path
            except UnicodeDecodeError:
                try:
                    with open(local_path, "r", encoding="latin-1") as f:
                        content = f.read()
                    source_label = local_path
                    st.info("File wasn't UTF-8 — decoded as Latin-1 instead.")
                except Exception as e:
                    st.error(f"Couldn't decode file: {e}")
            except PermissionError:
                st.error("Permission denied. You don't have rights to read this file.")
            except IsADirectoryError:
                st.error("That path is a directory, not a file.")
            except OSError as e:
                st.error(f"OS error while reading the file: {e}")

# ---------------------------------------------------------------------------
# Show content + find/replace
# ---------------------------------------------------------------------------

if content is not None:
    if content == "":
        st.warning(f"'{source_label}' is empty. Nothing to find/replace.")
    else:
        st.subheader("Original content")
        st.text_area("original", content, height=200, disabled=True, label_visibility="collapsed")

        st.subheader("Find & Replace")
        col1, col2 = st.columns(2)
        with col1:
            find_word = st.text_input("Find")
        with col2:
            replace_word = st.text_input("Replace with")

        col3, col4 = st.columns(2)
        with col3:
            case_sensitive = st.checkbox("Case sensitive", value=True)
        with col4:
            whole_word_only = st.checkbox("Whole word only", value=False)

        run_replace = st.button("🔍 Preview replacement", type="primary")

        if run_replace:
            if not find_word:
                st.warning("Enter a word or phrase to find.")
            else:
                import re

                try:
                    if whole_word_only:
                        pattern = r"\b" + re.escape(find_word) + r"\b"
                    else:
                        pattern = re.escape(find_word)

                    flags = 0 if case_sensitive else re.IGNORECASE
                    compiled = re.compile(pattern, flags)
                    match_count = len(compiled.findall(content))

                    if match_count == 0:
                        st.info(f"No occurrences of '{find_word}' found. Nothing to change.")
                        st.session_state["modified_content"] = None
                    else:
                        new_content = compiled.sub(replace_word, content)
                        st.session_state["modified_content"] = new_content
                        st.session_state["match_count"] = match_count
                        st.success(f"Found and replaced {match_count} occurrence(s).")
                except re.error as e:
                    st.error(f"Invalid find pattern: {e}")

        modified_content = st.session_state.get("modified_content")

        if modified_content is not None:
            st.subheader("Preview after replacement")
            st.text_area("modified", modified_content, height=200, disabled=True, label_visibility="collapsed")

            st.subheader("Save changes")
            save_col1, save_col2 = st.columns(2)

            with save_col1:
                st.download_button(
                    "⬇️ Download modified file",
                    data=modified_content.encode("utf-8"),
                    file_name=f"modified_{os.path.basename(source_label)}"
                    if source_label
                    else "modified_output.txt",
                    mime="text/plain",
                )

            with save_col2:
                if mode == "Read from a local file path" and local_path:
                    if st.button("💾 Overwrite original file on disk"):
                        try:
                            with open(local_path, "w", encoding="utf-8") as f:
                                f.write(modified_content)
                            st.success(f"Saved changes back to {local_path}")
                        except PermissionError:
                            st.error("Permission denied. Can't write to this path.")
                        except OSError as e:
                            st.error(f"OS error while saving: {e}")
                else:
                    st.caption(
                        "Overwrite-in-place is only available in "
                        "'Read from a local file path' mode."
                    )
