from enum import Enum, unique
from typing import List

__all__ = [
    "Kingdom",
    "TAXONOMIC_RANKS",
]


@unique
class Kingdom(str, Enum):
    """Enumeration of valid Darwin Core kingdoms."""

    ANIMALIA = "Animalia"
    PLANTAE = "Plantae"
    FUNGI = "Fungi"
    PROTISTA = "Protista"
    CHROMISTA = "Chromista"
    ARCHAEA = "Archaea"
    BACTERIA = "Bacteria"
    VIRUSES = "Viruses"
    INCERTAE_SEDIS = "incertae_sedis"

    def __str__(self) -> str:
        return str(self.value)


# See: https://dwc.tdwg.org/terms/#taxon
TAXONOMIC_RANKS: List[str] = [
    "domain",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
    "subspecies",
    "variety",
    "form",
] 