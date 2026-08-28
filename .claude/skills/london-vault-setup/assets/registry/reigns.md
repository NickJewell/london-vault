---
type: registry
registry: reigns
---

# Registry — Monarchs & Reigns

Lookup table for resolving reign-relative dates (schema §7). When a text says "in the reign of
Richard II", read the range from this table and write `date-range: 1377/1399` — **never recall a
reign range from memory.** Memory for regnal dates is exactly the kind of thing that is right
often enough to feel safe and wrong often enough to poison a timeline, and a wrong range is
invisible once it is in frontmatter.

Ranges are accession year / end-of-reign year. Where a reign is interrupted (Henry VI, Edward IV,
Æthelred), both stretches are given: use the one the passage is about, or the full outer span if
the text is not specific.

Keep the original phrasing in the note body ("in the reign of Richard II"), because the resolved
range is an interpretation and a later reader needs to see what it was derived from.

## Anglo-Saxon and Danish (London relevance from Alfred's restoration onward)

Kings of England before 1066 held London only intermittently, and before Alfred the settlement
in question is usually [[Lundenwic]] under Mercian or Kentish overlordship. For pre-886 material,
prefer the century range over a reign range and flag `#flag/ambiguous-date` if the text leans on
a ruler's reign for its dating.

| Monarch | Reign |
|---|---|
| Æthelberht of Kent | c. 589/616 |
| Offa of Mercia | 757/796 |
| Alfred the Great | 871/899 |
| Edward the Elder | 899/924 |
| Æthelstan | 924/939 |
| Edmund I | 939/946 |
| Eadred | 946/955 |
| Eadwig | 955/959 |
| Edgar the Peaceful | 959/975 |
| Edward the Martyr | 975/978 |
| Æthelred the Unready | 978/1013 and 1014/1016 |
| Sweyn Forkbeard | 1013/1014 |
| Edmund Ironside | 1016 |
| Cnut | 1016/1035 |
| Harold I Harefoot | 1035/1040 |
| Harthacnut | 1040/1042 |
| Edward the Confessor | 1042/1066 |
| Harold II Godwinson | 1066 |

## Norman

| Monarch | Reign |
|---|---|
| William I (the Conqueror) | 1066/1087 |
| William II (Rufus) | 1087/1100 |
| Henry I | 1100/1135 |
| Stephen | 1135/1154 |

The Anarchy (Stephen vs. the Empress Matilda) runs c. 1138/1153 inside Stephen's reign; Matilda
was never crowned, so "in the Empress's time" resolves to `date-range: 1141/1148` with the
phrasing preserved and `#flag/ambiguous-date`.

## Plantagenet

| Monarch | Reign |
|---|---|
| Henry II | 1154/1189 |
| Richard I | 1189/1199 |
| John | 1199/1216 |
| Henry III | 1216/1272 |
| Edward I | 1272/1307 |
| Edward II | 1307/1327 |
| Edward III | 1327/1377 |
| Richard II | 1377/1399 |

## Lancaster and York

| Monarch | Reign |
|---|---|
| Henry IV | 1399/1413 |
| Henry V | 1413/1422 |
| Henry VI | 1422/1461 and 1470/1471 |
| Edward IV | 1461/1470 and 1471/1483 |
| Edward V | 1483 |
| Richard III | 1483/1485 |

## Tudor

| Monarch | Reign |
|---|---|
| Henry VII | 1485/1509 |
| Henry VIII | 1509/1547 |
| Edward VI | 1547/1553 |
| Jane | 1553 (nine days; disputed) |
| Mary I | 1553/1558 |
| Elizabeth I | 1558/1603 |

Mary I and Philip reigned jointly 1554/1558; "in Philip and Mary's reign" resolves to that range.

## Stuart, Interregnum, and Restoration

| Monarch | Reign |
|---|---|
| James I | 1603/1625 |
| Charles I | 1625/1649 |
| **Interregnum / Commonwealth** | 1649/1660 |
| — Oliver Cromwell, Lord Protector | 1653/1658 |
| — Richard Cromwell, Lord Protector | 1658/1659 |
| Charles II | 1660/1685 |
| James II | 1685/1688 |
| William III & Mary II (jointly) | 1689/1694 |
| William III (alone) | 1694/1702 |
| Anne | 1702/1714 |

Charles II's *regnal* years are counted from his father's execution in 1649, so a document dated
"the twelfth year of Charles II" is 1660, not 1672. If a text gives a regnal year rather than a
calendar year, convert from the accession date, show the working in the body, and flag
`#flag/ambiguous-date` if the accession month matters.

## Hanover

| Monarch | Reign |
|---|---|
| George I | 1714/1727 |
| George II | 1727/1760 |
| George III | 1760/1820 |
| George IV | 1820/1830 |
| William IV | 1830/1837 |
| Victoria | 1837/1901 |

The Regency (George, Prince of Wales, acting for George III) runs 1811/1820. "Regency London" in
a text usually means the looser cultural period c. 1795/1837 — resolve to the strict 1811/1820
only when the text means the constitutional regency, and say which in the body.

## Windsor

| Monarch | Reign |
|---|---|
| Edward VII | 1901/1910 |
| George V | 1910/1936 |
| Edward VIII | 1936 |
| George VI | 1936/1952 |
| Elizabeth II | 1952/2022 |
| Charles III | 2022/ |

## Other reign-adjacent phrasings

| Phrasing in text | Resolution |
|---|---|
| "the Conquest" | `date: 1066` |
| "the Anarchy" | `date-range: 1138/1153` |
| "the Black Death" (London) | `date-range: 1348/1350` |
| "the Peasants' Revolt" | `date: 1381` |
| "the Civil War" | `date-range: 1642/1651` |
| "the Great Plague" | `date: 1665` |
| "the Great Fire" | `date-range: 1666-09-02/1666-09-06` |
| "the Blitz" | `date-range: 1940-09-07/1941-05-11` |

Anything not in this table that a source dates by event rather than year: resolve if you are
certain, otherwise record the phrase, add `#flag/ambiguous-date`, and let the user rule on it.
