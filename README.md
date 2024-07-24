# freeTranslate



this is intend to use google translate to get dataset from one language to another.

currently support cn -> en.

how to use:

prepare your dataset in pkl file with field:
cn: original text
en: None

the function `translate_doc` will read the text and translate as many `cn` values  as it can.