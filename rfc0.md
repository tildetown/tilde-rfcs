# RFC 0: (aka Standard 1) Markdown Tilde-RFC format

|Metadata||
|-|-|
|Author|Robert Miles (minerobber)|
|Status|Approved|
## Abstract

This RFC (number 0, known as Standard 1 in Markdown and Standard 1.1 in Plaintext) defines the format used by a Tilde-RFC when in Markdown.

Markdown Tilde-RFC files MAY be stored with any extension commonly used by markdown files.

## Format

A markdown Tilde-RFC file (hereinafter "markdown RFC") MUST start in a certain way. This is for metadata.

The first line MUST be the title, in the format of "# RFC (number): (name)".

Next should be a table with certain keys in a certain order:

The first value MUST be the author's name, and MAY include their email. This value MUST have the key "Author".

The next value MUST be the status of the RFC. This value MUST have the key "Status"

The next values are optional, and MAY or MAY NOT be included.

The first of these optional values is a list of the RFCs updated by this text RFC. It must have the key "Updates". (i.e; "|Updates|13, 35|")

The next is a list of the RFCs that update this text RFC. (i.e; "|Updated by|40|")

The last of these optional lines, if included, MUST be equal to "|Notice|Errata Exist|". This indicates that the document contains errors.

The lines after the required lines and included optional lines are the content. (see: the source of this document)
