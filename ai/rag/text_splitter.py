import re


class StructureAwareTextSplitter:
    """
    Splits text using document structure first.

    Strategy:
    1. Respect Markdown-style headings when available.
    2. Recursively split oversized sections using:
       paragraphs -> lines -> sentences -> words.
    3. Apply overlap only once after splitting.
    """

    def __init__(self, chunk_size=1200, overlap=150):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        if not text or not text.strip():
            return []

        text = text.strip()

        # Structure-aware split using Markdown headings
        sections = re.split(
            r"(?=^#{1,6}\s+.+$)",
            text,
            flags=re.MULTILINE
        )

        base_chunks = []

        for section in sections:
            section = section.strip()

            if not section:
                continue

            if len(section) <= self.chunk_size:
                base_chunks.append(section)
            else:
                base_chunks.extend(
                    self._recursive_split(
                        section,
                        separators=[
                            "\n\n",
                            "\n",
                            ". ",
                            " "
                        ]
                    )
                )

        # Apply overlap ONCE here
        return self._apply_overlap(base_chunks)

    def _recursive_split(self, text, separators):
        """
        Split text into chunks without overlap.
        """

        text = text.strip()

        if len(text) <= self.chunk_size:
            return [text]

        # Final fallback
        if not separators:
            return [
                text[i:i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size)
            ]

        separator = separators[0]
        remaining_separators = separators[1:]

        parts = text.split(separator)

        # If this separator cannot split the text,
        # move to the next separator.
        if len(parts) == 1:
            return self._recursive_split(
                text,
                remaining_separators
            )

        chunks = []
        current = ""

        for part in parts:
            part = part.strip()

            if not part:
                continue

            # Re-add natural separator where useful
            if separator == ". ":
                part = part + "."

            candidate = (
                part
                if not current
                else current + separator + part
            )

            if len(candidate) <= self.chunk_size:
                current = candidate

            else:
                if current:
                    chunks.append(current.strip())

                # This individual part is still too large
                if len(part) > self.chunk_size:
                    smaller_chunks = self._recursive_split(
                        part,
                        remaining_separators
                    )

                    chunks.extend(smaller_chunks)
                    current = ""
                else:
                    current = part

        if current:
            chunks.append(current.strip())

        return chunks

    def _apply_overlap(self, chunks):
        """
        Add overlap between neighboring chunks exactly once.
        """

        if not chunks:
            return []

        if self.overlap == 0:
            return chunks

        final_chunks = [chunks[0]]

        for i in range(1, len(chunks)):
            previous = final_chunks[-1]
            current = chunks[i]

            overlap_text = previous[-self.overlap:].strip()

            # Avoid adding text that is already at the
            # beginning of the next chunk.
            if overlap_text and not current.startswith(overlap_text):
                combined = overlap_text + " " + current
            else:
                combined = current

            final_chunks.append(combined.strip())

        return final_chunks