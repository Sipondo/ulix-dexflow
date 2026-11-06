from functools import lru_cache
from io import BytesIO

from fontTools.ttLib import TTFont

PAIR_ADJUSTMENT = 2
EXTENSION = 9


class KerningTable:
    def __init__(self, data):
        font = TTFont(BytesIO(data))
        self.units_per_em = font['head'].unitsPerEm
        self.cmap = font.getBestCmap()
        self._subtables = _gpos_kern_subtables(font) if 'GPOS' in font else []
        self._legacy = {}
        if not self._subtables and 'kern' in font:
            for table in font['kern'].kernTables:
                if getattr(table, 'format', None) == 0:
                    self._legacy.update(table.kernTable)

    def has_char(self, char):
        return ord(char) in self.cmap

    @lru_cache(maxsize=4096)
    def get(self, left, right):
        a, b = self.cmap.get(ord(left)), self.cmap.get(ord(right))
        if a is None or b is None:
            return 0
        if not self._subtables:
            return self._legacy.get((a, b), 0)

        total = 0
        for lookup in self._subtables:
            for subtable in lookup:
                value = _pair_value(subtable, a, b)
                if value is not None:
                    total += value
                    break
        return total


def _gpos_kern_subtables(font):
    gpos = font['GPOS'].table
    if not gpos.FeatureList or not gpos.LookupList:
        return []
    indices = sorted(
        {
            index
            for record in gpos.FeatureList.FeatureRecord
            if record.FeatureTag == 'kern'
            for index in record.Feature.LookupListIndex
        }
    )
    lookups = []
    for index in indices:
        lookup = gpos.LookupList.Lookup[index]
        subtables = []
        for subtable in lookup.SubTable:
            if lookup.LookupType == EXTENSION:
                if subtable.ExtensionLookupType != PAIR_ADJUSTMENT:
                    continue
                subtable = subtable.ExtSubTable
            elif lookup.LookupType != PAIR_ADJUSTMENT:
                continue
            subtables.append(subtable)
        lookups.append(subtables)
    return lookups


def _x_advance(value_record):
    if value_record is None:
        return 0
    return getattr(value_record, 'XAdvance', 0) or 0


def _pair_value(subtable, left, right):
    if left not in subtable.Coverage.glyphs:
        return None
    if subtable.Format == 1:
        pair_set = subtable.PairSet[subtable.Coverage.glyphs.index(left)]
        for record in pair_set.PairValueRecord:
            if record.SecondGlyph == right:
                return _x_advance(record.Value1)
        return None
    if subtable.Format == 2:
        class1 = subtable.ClassDef1.classDefs.get(left, 0)
        class2 = subtable.ClassDef2.classDefs.get(right, 0)
        return _x_advance(subtable.Class1Record[class1].Class2Record[class2].Value1)
    return None
