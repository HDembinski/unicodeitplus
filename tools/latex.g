start: (item | math)*

?atom: CHARACTER
    | COMMAND

?item: atom
    | WS+
    | group

CHARACTER: /[^%#&\{\}^_]/ | ESCAPED
ESCAPED: "\\\\" | "\\#" | "\\%" | "\\&"  | "\\{" | "\\}" | "\\_" | "\\,"
group: "{" item* "}"
math: "$" item* "$"
SUBSCRIPT: "_"
SUPERSCRIPT: "^"
COMMAND: (("\\" WORD WS*) | SUBSCRIPT | SUPERSCRIPT)

%import common.WS
%import common.WORD
