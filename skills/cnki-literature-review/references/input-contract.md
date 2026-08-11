# Input contract

The pipeline accepts UTF-8 JSON or CSV containing bibliographic records supplied
by the user.

## Required field

- `title`: non-empty article or chapter title.

## Optional fields

- `authors`: list or a string separated by commas, semicolons, `；`, or `、`.
- `year`: four-digit publication year.
- `journal` or `source`: publication name.
- `keywords`: list or separated string.
- `abstract`: abstract the user is permitted to process.
- `citations`: non-negative displayed citation count; only a secondary ranking
  signal and never a quality verdict.
- `locator`: DOI, stable public record URL, or user-defined reference key.
- `notes`: the user's own reading notes or short permitted excerpts.

JSON may be a list of records or an object with a `records` list. CSV uses the
same field names in its header. Unknown fields are ignored.

Do not place credentials, browser-session data, signed download links, private
manuscripts, or bundled source documents in the input.
