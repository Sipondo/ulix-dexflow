# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = ldtk_json_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import List, Any, Optional, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


class AllowedRefs(Enum):
    """Possible values: `Any`, `OnlySame`, `OnlyTags`"""

    ANY = "Any"
    ONLY_SAME = "OnlySame"
    ONLY_TAGS = "OnlyTags"


class EditorDisplayMode(Enum):
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`,
    `ArrayCountWithLabel`, `ArrayCountNoLabel`, `RefLinkBetweenPivots`,
    `RefLinkBetweenCenters`
    """

    ARRAY_COUNT_NO_LABEL = "ArrayCountNoLabel"
    ARRAY_COUNT_WITH_LABEL = "ArrayCountWithLabel"
    ENTITY_TILE = "EntityTile"
    HIDDEN = "Hidden"
    NAME_AND_VALUE = "NameAndValue"
    POINTS = "Points"
    POINT_PATH = "PointPath"
    POINT_PATH_LOOP = "PointPathLoop"
    POINT_STAR = "PointStar"
    RADIUS_GRID = "RadiusGrid"
    RADIUS_PX = "RadiusPx"
    REF_LINK_BETWEEN_CENTERS = "RefLinkBetweenCenters"
    REF_LINK_BETWEEN_PIVOTS = "RefLinkBetweenPivots"
    VALUE_ONLY = "ValueOnly"


class EditorDisplayPos(Enum):
    """Possible values: `Above`, `Center`, `Beneath`"""

    ABOVE = "Above"
    BENEATH = "Beneath"
    CENTER = "Center"


class LevelFieldType(Enum):
    """Internal type enum Possible values: `F_Int`, `F_Float`, `F_String`, `F_Text`, `F_Bool`,
    `F_Color`, `F_Enum`, `F_Point`, `F_Path`, `F_EntityRef`, `F_Tile`
    """

    F_BOOL = "F_Bool"
    F_COLOR = "F_Color"
    F_ENTITY_REF = "F_EntityRef"
    F_ENUM = "F_Enum"
    F_FLOAT = "F_Float"
    F_INT = "F_Int"
    F_PATH = "F_Path"
    F_POINT = "F_Point"
    F_STRING = "F_String"
    F_TEXT = "F_Text"
    F_TILE = "F_Tile"


class TextLanguageMode(Enum):
    LANG_C = "LangC"
    LANG_HAXE = "LangHaxe"
    LANG_JS = "LangJS"
    LANG_JSON = "LangJson"
    LANG_LOG = "LangLog"
    LANG_LUA = "LangLua"
    LANG_MARKDOWN = "LangMarkdown"
    LANG_PYTHON = "LangPython"
    LANG_RUBY = "LangRuby"
    LANG_XML = "LangXml"


@dataclass
class FieldDefinition:
    """This section is mostly only intended for the LDtk editor app itself. You can safely
    ignore it.
    """

    """Human readable value type. Possible values: `Int, Float, String, Bool, Color,
    ExternEnum.XXX, LocalEnum.XXX, Point, FilePath`.<br/>  If the field is an array, this
    field will look like `Array<...>` (eg. `Array<Int>`, `Array<Point>` etc.)<br/>  NOTE: if
    you enable the advanced option **Use Multilines type**, you will have "*Multilines*"
    instead of "*String*" when relevant.
    """
    type: str
    """Possible values: `Any`, `OnlySame`, `OnlyTags`"""
    allowed_refs: AllowedRefs
    allowed_ref_tags: List[str]
    allow_out_of_level_ref: bool
    auto_chain_ref: bool
    """TRUE if the value can be null. For arrays, TRUE means it can contain null values
    (exception: array of Points can't have null values).
    """
    can_be_null: bool
    """Default value if selected value is null or invalid."""
    default_override: Any
    editor_always_show: bool
    editor_cut_long_values: bool
    """Possible values: `Hidden`, `ValueOnly`, `NameAndValue`, `EntityTile`, `Points`,
    `PointStar`, `PointPath`, `PointPathLoop`, `RadiusPx`, `RadiusGrid`,
    `ArrayCountWithLabel`, `ArrayCountNoLabel`, `RefLinkBetweenPivots`,
    `RefLinkBetweenCenters`
    """
    editor_display_mode: EditorDisplayMode
    """Possible values: `Above`, `Center`, `Beneath`"""
    editor_display_pos: EditorDisplayPos
    """User defined unique identifier"""
    identifier: str
    """TRUE if the value is an array of multiple values"""
    is_array: bool
    symmetrical_ref: bool
    """Internal type enum Possible values: `F_Int`, `F_Float`, `F_String`, `F_Text`, `F_Bool`,
    `F_Color`, `F_Enum`, `F_Point`, `F_Path`, `F_EntityRef`, `F_Tile`
    """
    field_definition_type: LevelFieldType
    """Unique Int identifier"""
    uid: int
    """If TRUE, the color associated with this field will override the Entity or Level default
    color in the editor UI. For Enum fields, this would be the color associated to their
    values.
    """
    use_for_smart_color: bool
    """Optional list of accepted file extensions for FilePath value type. Includes the dot:
    `.ext`
    """
    accept_file_types: Optional[List[str]] = None
    """Array max length"""
    array_max_length: Optional[int] = None
    """Array min length"""
    array_min_length: Optional[int] = None
    editor_text_prefix: Optional[str] = None
    editor_text_suffix: Optional[str] = None
    """Max limit for value, if applicable"""
    max: Optional[float] = None
    """Min limit for value, if applicable"""
    min: Optional[float] = None
    """Optional regular expression that needs to be matched to accept values. Expected format:
    `/some_reg_ex/g`, with optional "i" flag.
    """
    regex: Optional[str] = None
    """Possible values: &lt;`null`&gt;, `LangPython`, `LangRuby`, `LangJS`, `LangLua`, `LangC`,
    `LangHaxe`, `LangMarkdown`, `LangJson`, `LangXml`, `LangLog`
    """
    text_language_mode: Optional[TextLanguageMode] = None
    """UID of the tileset used for a Tile"""
    tileset_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "FieldDefinition":
        assert isinstance(obj, dict)
        type = from_str(obj.get("__type"))
        allowed_refs = AllowedRefs(obj.get("allowedRefs"))
        allowed_ref_tags = from_list(from_str, obj.get("allowedRefTags"))
        allow_out_of_level_ref = from_bool(obj.get("allowOutOfLevelRef"))
        auto_chain_ref = from_bool(obj.get("autoChainRef"))
        can_be_null = from_bool(obj.get("canBeNull"))
        default_override = obj.get("defaultOverride")
        editor_always_show = from_bool(obj.get("editorAlwaysShow"))
        editor_cut_long_values = from_bool(obj.get("editorCutLongValues"))
        editor_display_mode = EditorDisplayMode(obj.get("editorDisplayMode"))
        editor_display_pos = EditorDisplayPos(obj.get("editorDisplayPos"))
        identifier = from_str(obj.get("identifier"))
        is_array = from_bool(obj.get("isArray"))
        symmetrical_ref = from_bool(obj.get("symmetricalRef"))

        try:
            field_definition_type = LevelFieldType(obj.get("type"))
        except ValueError as e:
            field_definition_type = LevelFieldType(obj.get("type")["id"])

        uid = from_int(obj.get("uid"))
        use_for_smart_color = from_bool(obj.get("useForSmartColor"))
        accept_file_types = from_union(
            [from_none, lambda x: from_list(from_str, x)], obj.get("acceptFileTypes")
        )
        array_max_length = from_union([from_none, from_int], obj.get("arrayMaxLength"))
        array_min_length = from_union([from_none, from_int], obj.get("arrayMinLength"))
        editor_text_prefix = from_union(
            [from_none, from_str], obj.get("editorTextPrefix")
        )
        editor_text_suffix = from_union(
            [from_none, from_str], obj.get("editorTextSuffix")
        )
        max = from_union([from_none, from_float], obj.get("max"))
        min = from_union([from_none, from_float], obj.get("min"))
        regex = from_union([from_none, from_str], obj.get("regex"))
        text_language_mode = from_union(
            [from_none, TextLanguageMode], obj.get("textLanguageMode")
        )
        tileset_uid = from_union([from_none, from_int], obj.get("tilesetUid"))
        return FieldDefinition(
            type,
            allowed_refs,
            allowed_ref_tags,
            allow_out_of_level_ref,
            auto_chain_ref,
            can_be_null,
            default_override,
            editor_always_show,
            editor_cut_long_values,
            editor_display_mode,
            editor_display_pos,
            identifier,
            is_array,
            symmetrical_ref,
            field_definition_type,
            uid,
            use_for_smart_color,
            accept_file_types,
            array_max_length,
            array_min_length,
            editor_text_prefix,
            editor_text_suffix,
            max,
            min,
            regex,
            text_language_mode,
            tileset_uid,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_str(self.type)
        result["allowedRefs"] = to_enum(AllowedRefs, self.allowed_refs)
        result["allowedRefTags"] = from_list(from_str, self.allowed_ref_tags)
        result["allowOutOfLevelRef"] = from_bool(self.allow_out_of_level_ref)
        result["autoChainRef"] = from_bool(self.auto_chain_ref)
        result["canBeNull"] = from_bool(self.can_be_null)
        result["defaultOverride"] = self.default_override
        result["editorAlwaysShow"] = from_bool(self.editor_always_show)
        result["editorCutLongValues"] = from_bool(self.editor_cut_long_values)
        result["editorDisplayMode"] = to_enum(
            EditorDisplayMode, self.editor_display_mode
        )
        result["editorDisplayPos"] = to_enum(EditorDisplayPos, self.editor_display_pos)
        result["identifier"] = from_str(self.identifier)
        result["isArray"] = from_bool(self.is_array)
        result["symmetricalRef"] = from_bool(self.symmetrical_ref)
        result["type"] = to_enum(LevelFieldType, self.field_definition_type)
        result["uid"] = from_int(self.uid)
        result["useForSmartColor"] = from_bool(self.use_for_smart_color)
        result["acceptFileTypes"] = from_union(
            [from_none, lambda x: from_list(from_str, x)], self.accept_file_types
        )
        result["arrayMaxLength"] = from_union(
            [from_none, from_int], self.array_max_length
        )
        result["arrayMinLength"] = from_union(
            [from_none, from_int], self.array_min_length
        )
        result["editorTextPrefix"] = from_union(
            [from_none, from_str], self.editor_text_prefix
        )
        result["editorTextSuffix"] = from_union(
            [from_none, from_str], self.editor_text_suffix
        )
        result["max"] = from_union([from_none, to_float], self.max)
        result["min"] = from_union([from_none, to_float], self.min)
        result["regex"] = from_union([from_none, from_str], self.regex)
        result["textLanguageMode"] = from_union(
            [from_none, lambda x: to_enum(TextLanguageMode, x)], self.text_language_mode
        )
        result["tilesetUid"] = from_union([from_none, from_int], self.tileset_uid)
        return result


class LimitBehavior(Enum):
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""

    DISCARD_OLD_ONES = "DiscardOldOnes"
    MOVE_LAST_ONE = "MoveLastOne"
    PREVENT_ADDING = "PreventAdding"


class LimitScope(Enum):
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """

    PER_LAYER = "PerLayer"
    PER_LEVEL = "PerLevel"
    PER_WORLD = "PerWorld"


class RenderMode(Enum):
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""

    CROSS = "Cross"
    ELLIPSE = "Ellipse"
    RECTANGLE = "Rectangle"
    TILE = "Tile"


@dataclass
class TilesetRectangle:
    """This object represents a custom sub rectangle in a Tileset image."""

    """Height in pixels"""
    h: int
    """UID of the tileset"""
    tileset_uid: int
    """Width in pixels"""
    w: int
    """X pixels coordinate of the top-left corner in the Tileset image"""
    x: int
    """Y pixels coordinate of the top-left corner in the Tileset image"""
    y: int

    @staticmethod
    def from_dict(obj: Any) -> "TilesetRectangle":
        assert isinstance(obj, dict)
        h = from_int(obj.get("h"))
        tileset_uid = from_int(obj.get("tilesetUid"))
        w = from_int(obj.get("w"))
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        return TilesetRectangle(h, tileset_uid, w, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["h"] = from_int(self.h)
        result["tilesetUid"] = from_int(self.tileset_uid)
        result["w"] = from_int(self.w)
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        return result


class TileRenderMode(Enum):
    """Possible values: `Cover`, `FitInside`, `Repeat`, `Stretch`, `FullSizeCropped`,
    `FullSizeUncropped`
    """

    COVER = "Cover"
    FIT_INSIDE = "FitInside"
    FULL_SIZE_CROPPED = "FullSizeCropped"
    FULL_SIZE_UNCROPPED = "FullSizeUncropped"
    REPEAT = "Repeat"
    STRETCH = "Stretch"


@dataclass
class EntityDefinition:
    """Base entity color"""

    color: str
    """Array of field definitions"""
    field_defs: List[FieldDefinition]
    fill_opacity: float
    """Pixel height"""
    height: int
    hollow: bool
    """User defined unique identifier"""
    identifier: str
    """Only applies to entities resizable on both X/Y. If TRUE, the entity instance width/height
    will keep the same aspect ratio as the definition.
    """
    keep_aspect_ratio: bool
    """Possible values: `DiscardOldOnes`, `PreventAdding`, `MoveLastOne`"""
    limit_behavior: LimitBehavior
    """If TRUE, the maxCount is a "per world" limit, if FALSE, it's a "per level". Possible
    values: `PerLayer`, `PerLevel`, `PerWorld`
    """
    limit_scope: LimitScope
    line_opacity: float
    """Max instances count"""
    max_count: int
    """Pivot X coordinate (from 0 to 1.0)"""
    pivot_x: float
    """Pivot Y coordinate (from 0 to 1.0)"""
    pivot_y: float
    """Possible values: `Rectangle`, `Ellipse`, `Tile`, `Cross`"""
    render_mode: RenderMode
    """If TRUE, the entity instances will be resizable horizontally"""
    resizable_x: bool
    """If TRUE, the entity instances will be resizable vertically"""
    resizable_y: bool
    """Display entity name in editor"""
    show_name: bool
    """An array of strings that classifies this entity"""
    tags: List[str]
    tile_opacity: float
    """Possible values: `Cover`, `FitInside`, `Repeat`, `Stretch`, `FullSizeCropped`,
    `FullSizeUncropped`
    """
    tile_render_mode: TileRenderMode
    """Unique Int identifier"""
    uid: int
    """Pixel width"""
    width: int
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `tileRect`
    """
    tile_id: Optional[int] = None
    """An object representing a rectangle from an existing Tileset"""
    tile_rect: Optional[TilesetRectangle] = None
    """Tileset ID used for optional tile display"""
    tileset_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "EntityDefinition":
        assert isinstance(obj, dict)
        color = from_str(obj.get("color"))
        field_defs = from_list(FieldDefinition.from_dict, obj.get("fieldDefs"))
        fill_opacity = from_float(obj.get("fillOpacity"))
        height = from_int(obj.get("height"))
        hollow = from_bool(obj.get("hollow"))
        identifier = from_str(obj.get("identifier"))
        keep_aspect_ratio = from_bool(obj.get("keepAspectRatio"))
        limit_behavior = LimitBehavior(obj.get("limitBehavior"))
        limit_scope = LimitScope(obj.get("limitScope"))
        line_opacity = from_float(obj.get("lineOpacity"))
        max_count = from_int(obj.get("maxCount"))
        pivot_x = from_float(obj.get("pivotX"))
        pivot_y = from_float(obj.get("pivotY"))
        render_mode = RenderMode(obj.get("renderMode"))
        resizable_x = from_bool(obj.get("resizableX"))
        resizable_y = from_bool(obj.get("resizableY"))
        show_name = from_bool(obj.get("showName"))
        tags = from_list(from_str, obj.get("tags"))
        tile_opacity = from_float(obj.get("tileOpacity"))
        tile_render_mode = TileRenderMode(obj.get("tileRenderMode"))
        uid = from_int(obj.get("uid"))
        width = from_int(obj.get("width"))
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        tile_rect = from_union(
            [from_none, TilesetRectangle.from_dict], obj.get("tileRect")
        )
        tileset_id = from_union([from_none, from_int], obj.get("tilesetId"))
        return EntityDefinition(
            color,
            field_defs,
            fill_opacity,
            height,
            hollow,
            identifier,
            keep_aspect_ratio,
            limit_behavior,
            limit_scope,
            line_opacity,
            max_count,
            pivot_x,
            pivot_y,
            render_mode,
            resizable_x,
            resizable_y,
            show_name,
            tags,
            tile_opacity,
            tile_render_mode,
            uid,
            width,
            tile_id,
            tile_rect,
            tileset_id,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_str(self.color)
        result["fieldDefs"] = from_list(
            lambda x: to_class(FieldDefinition, x), self.field_defs
        )
        result["fillOpacity"] = to_float(self.fill_opacity)
        result["height"] = from_int(self.height)
        result["hollow"] = from_bool(self.hollow)
        result["identifier"] = from_str(self.identifier)
        result["keepAspectRatio"] = from_bool(self.keep_aspect_ratio)
        result["limitBehavior"] = to_enum(LimitBehavior, self.limit_behavior)
        result["limitScope"] = to_enum(LimitScope, self.limit_scope)
        result["lineOpacity"] = to_float(self.line_opacity)
        result["maxCount"] = from_int(self.max_count)
        result["pivotX"] = to_float(self.pivot_x)
        result["pivotY"] = to_float(self.pivot_y)
        result["renderMode"] = to_enum(RenderMode, self.render_mode)
        result["resizableX"] = from_bool(self.resizable_x)
        result["resizableY"] = from_bool(self.resizable_y)
        result["showName"] = from_bool(self.show_name)
        result["tags"] = from_list(from_str, self.tags)
        result["tileOpacity"] = to_float(self.tile_opacity)
        result["tileRenderMode"] = to_enum(TileRenderMode, self.tile_render_mode)
        result["uid"] = from_int(self.uid)
        result["width"] = from_int(self.width)
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        result["tileRect"] = from_union(
            [from_none, lambda x: to_class(TilesetRectangle, x)], self.tile_rect
        )
        result["tilesetId"] = from_union([from_none, from_int], self.tileset_id)
        return result


@dataclass
class EnumValueDefinition:
    """Optional color"""

    color: int
    """Enum value"""
    id: str
    """An array of 4 Int values that refers to the tile in the tileset image: `[ x, y, width,
    height ]`
    """
    tile_src_rect: Optional[List[int]] = None
    """The optional ID of the tile"""
    tile_id: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "EnumValueDefinition":
        assert isinstance(obj, dict)
        color = from_int(obj.get("color"))
        id = from_str(obj.get("id"))
        tile_src_rect = from_union(
            [from_none, lambda x: from_list(from_int, x)], obj.get("__tileSrcRect")
        )
        tile_id = from_union([from_none, from_int], obj.get("tileId"))
        return EnumValueDefinition(color, id, tile_src_rect, tile_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_int(self.color)
        result["id"] = from_str(self.id)
        result["__tileSrcRect"] = from_union(
            [from_none, lambda x: from_list(from_int, x)], self.tile_src_rect
        )
        result["tileId"] = from_union([from_none, from_int], self.tile_id)
        return result


@dataclass
class EnumDefinition:
    """User defined unique identifier"""

    identifier: str
    """An array of user-defined tags to organize the Enums"""
    tags: List[str]
    """Unique Int identifier"""
    uid: int
    """All possible enum values, with their optional Tile infos."""
    values: List[EnumValueDefinition]
    external_file_checksum: Optional[str] = None
    """Relative path to the external file providing this Enum"""
    external_rel_path: Optional[str] = None
    """Tileset UID if provided"""
    icon_tileset_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "EnumDefinition":
        assert isinstance(obj, dict)
        identifier = from_str(obj.get("identifier"))
        tags = from_list(from_str, obj.get("tags"))
        uid = from_int(obj.get("uid"))
        values = from_list(EnumValueDefinition.from_dict, obj.get("values"))
        external_file_checksum = from_union(
            [from_none, from_str], obj.get("externalFileChecksum")
        )
        external_rel_path = from_union(
            [from_none, from_str], obj.get("externalRelPath")
        )
        icon_tileset_uid = from_union([from_none, from_int], obj.get("iconTilesetUid"))
        return EnumDefinition(
            identifier,
            tags,
            uid,
            values,
            external_file_checksum,
            external_rel_path,
            icon_tileset_uid,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = from_str(self.identifier)
        result["tags"] = from_list(from_str, self.tags)
        result["uid"] = from_int(self.uid)
        result["values"] = from_list(
            lambda x: to_class(EnumValueDefinition, x), self.values
        )
        result["externalFileChecksum"] = from_union(
            [from_none, from_str], self.external_file_checksum
        )
        result["externalRelPath"] = from_union(
            [from_none, from_str], self.external_rel_path
        )
        result["iconTilesetUid"] = from_union(
            [from_none, from_int], self.icon_tileset_uid
        )
        return result


class Checker(Enum):
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""

    HORIZONTAL = "Horizontal"
    NONE = "None"
    VERTICAL = "Vertical"


class TileMode(Enum):
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""

    SINGLE = "Single"
    STAMP = "Stamp"


@dataclass
class AutoLayerRuleDefinition:
    """This complex section isn't meant to be used by game devs at all, as these rules are
    completely resolved internally by the editor before any saving. You should just ignore
    this part.
    """

    """If FALSE, the rule effect isn't applied, and no tiles are generated."""
    active: bool
    """When TRUE, the rule will prevent other rules to be applied in the same cell if it matches
    (TRUE by default).
    """
    break_on_match: bool
    """Chances for this rule to be applied (0 to 1)"""
    chance: float
    """Checker mode Possible values: `None`, `Horizontal`, `Vertical`"""
    checker: Checker
    """If TRUE, allow rule to be matched by flipping its pattern horizontally"""
    flip_x: bool
    """If TRUE, allow rule to be matched by flipping its pattern vertically"""
    flip_y: bool
    """Rule pattern (size x size)"""
    pattern: List[int]
    """If TRUE, enable Perlin filtering to only apply rule on specific random area"""
    perlin_active: bool
    perlin_octaves: float
    perlin_scale: float
    perlin_seed: float
    """X pivot of a tile stamp (0-1)"""
    pivot_x: float
    """Y pivot of a tile stamp (0-1)"""
    pivot_y: float
    """Pattern width & height. Should only be 1,3,5 or 7."""
    size: int
    """Array of all the tile IDs. They are used randomly or as stamps, based on `tileMode` value."""
    tile_ids: List[int]
    """Defines how tileIds array is used Possible values: `Single`, `Stamp`"""
    tile_mode: TileMode
    """Unique Int identifier"""
    uid: int
    """X cell coord modulo"""
    x_modulo: int
    """X cell start offset"""
    x_offset: int
    """Y cell coord modulo"""
    y_modulo: int
    """Y cell start offset"""
    y_offset: int
    """Default IntGrid value when checking cells outside of level bounds"""
    out_of_bounds_value: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "AutoLayerRuleDefinition":
        assert isinstance(obj, dict)
        active = from_bool(obj.get("active"))
        break_on_match = from_bool(obj.get("breakOnMatch"))
        chance = from_float(obj.get("chance"))
        checker = Checker(obj.get("checker"))
        flip_x = from_bool(obj.get("flipX"))
        flip_y = from_bool(obj.get("flipY"))
        pattern = from_list(from_int, obj.get("pattern"))
        perlin_active = from_bool(obj.get("perlinActive"))
        perlin_octaves = from_float(obj.get("perlinOctaves"))
        perlin_scale = from_float(obj.get("perlinScale"))
        perlin_seed = from_float(obj.get("perlinSeed"))
        pivot_x = from_float(obj.get("pivotX"))
        pivot_y = from_float(obj.get("pivotY"))
        size = from_int(obj.get("size"))
        tile_ids = from_list(from_int, obj.get("tileIds"))
        tile_mode = TileMode(obj.get("tileMode"))
        uid = from_int(obj.get("uid"))
        x_modulo = from_int(obj.get("xModulo"))
        x_offset = from_int(obj.get("xOffset"))
        y_modulo = from_int(obj.get("yModulo"))
        y_offset = from_int(obj.get("yOffset"))
        out_of_bounds_value = from_union(
            [from_none, from_int], obj.get("outOfBoundsValue")
        )
        return AutoLayerRuleDefinition(
            active,
            break_on_match,
            chance,
            checker,
            flip_x,
            flip_y,
            pattern,
            perlin_active,
            perlin_octaves,
            perlin_scale,
            perlin_seed,
            pivot_x,
            pivot_y,
            size,
            tile_ids,
            tile_mode,
            uid,
            x_modulo,
            x_offset,
            y_modulo,
            y_offset,
            out_of_bounds_value,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_bool(self.active)
        result["breakOnMatch"] = from_bool(self.break_on_match)
        result["chance"] = to_float(self.chance)
        result["checker"] = to_enum(Checker, self.checker)
        result["flipX"] = from_bool(self.flip_x)
        result["flipY"] = from_bool(self.flip_y)
        result["pattern"] = from_list(from_int, self.pattern)
        result["perlinActive"] = from_bool(self.perlin_active)
        result["perlinOctaves"] = to_float(self.perlin_octaves)
        result["perlinScale"] = to_float(self.perlin_scale)
        result["perlinSeed"] = to_float(self.perlin_seed)
        result["pivotX"] = to_float(self.pivot_x)
        result["pivotY"] = to_float(self.pivot_y)
        result["size"] = from_int(self.size)
        result["tileIds"] = from_list(from_int, self.tile_ids)
        result["tileMode"] = to_enum(TileMode, self.tile_mode)
        result["uid"] = from_int(self.uid)
        result["xModulo"] = from_int(self.x_modulo)
        result["xOffset"] = from_int(self.x_offset)
        result["yModulo"] = from_int(self.y_modulo)
        result["yOffset"] = from_int(self.y_offset)
        result["outOfBoundsValue"] = from_union(
            [from_none, from_int], self.out_of_bounds_value
        )
        return result


@dataclass
class AutoLayerRuleGroup:
    active: bool
    is_optional: bool
    name: str
    rules: List[AutoLayerRuleDefinition]
    uid: int
    """*This field was removed in 1.0.0 and should no longer be used.*"""
    collapsed: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "AutoLayerRuleGroup":
        assert isinstance(obj, dict)
        active = from_bool(obj.get("active"))
        is_optional = from_bool(obj.get("isOptional"))
        name = from_str(obj.get("name"))
        rules = from_list(AutoLayerRuleDefinition.from_dict, obj.get("rules"))
        uid = from_int(obj.get("uid"))
        collapsed = from_union([from_none, from_bool], obj.get("collapsed"))
        return AutoLayerRuleGroup(active, is_optional, name, rules, uid, collapsed)

    def to_dict(self) -> dict:
        result: dict = {}
        result["active"] = from_bool(self.active)
        result["isOptional"] = from_bool(self.is_optional)
        result["name"] = from_str(self.name)
        result["rules"] = from_list(
            lambda x: to_class(AutoLayerRuleDefinition, x), self.rules
        )
        result["uid"] = from_int(self.uid)
        result["collapsed"] = from_union([from_none, from_bool], self.collapsed)
        return result


@dataclass
class IntGridValueDefinition:
    """IntGrid value definition"""

    color: str
    """The IntGrid value itself"""
    value: int
    """User defined unique identifier"""
    identifier: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "IntGridValueDefinition":
        assert isinstance(obj, dict)
        color = from_str(obj.get("color"))
        value = from_int(obj.get("value"))
        identifier = from_union([from_none, from_str], obj.get("identifier"))
        return IntGridValueDefinition(color, value, identifier)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_str(self.color)
        result["value"] = from_int(self.value)
        result["identifier"] = from_union([from_none, from_str], self.identifier)
        return result


class LayerType(Enum):
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """

    AUTO_LAYER = "AutoLayer"
    ENTITIES = "Entities"
    INT_GRID = "IntGrid"
    TILES = "Tiles"


@dataclass
class LayerDefinition:
    """Type of the layer (*IntGrid, Entities, Tiles or AutoLayer*)"""

    type: str
    """Contains all the auto-layer rule definitions."""
    auto_rule_groups: List[AutoLayerRuleGroup]
    """Opacity of the layer (0 to 1.0)"""
    display_opacity: float
    """An array of tags to forbid some Entities in this layer"""
    excluded_tags: List[str]
    """Width and height of the grid in pixels"""
    grid_size: int
    """Height of the optional "guide" grid in pixels"""
    guide_grid_hei: int
    """Width of the optional "guide" grid in pixels"""
    guide_grid_wid: int
    hide_fields_when_inactive: bool
    """Hide the layer from the list on the side of the editor view."""
    hide_in_list: bool
    """User defined unique identifier"""
    identifier: str
    """Alpha of this layer when it is not the active one."""
    inactive_opacity: float
    """An array that defines extra optional info for each IntGrid value.<br/>  WARNING: the
    array order is not related to actual IntGrid values! As user can re-order IntGrid values
    freely, you may value "2" before value "1" in this array.
    """
    int_grid_values: List[IntGridValueDefinition]
    """Parallax horizontal factor (from -1 to 1, defaults to 0) which affects the scrolling
    speed of this layer, creating a fake 3D (parallax) effect.
    """
    parallax_factor_x: float
    """Parallax vertical factor (from -1 to 1, defaults to 0) which affects the scrolling speed
    of this layer, creating a fake 3D (parallax) effect.
    """
    parallax_factor_y: float
    """If true (default), a layer with a parallax factor will also be scaled up/down accordingly."""
    parallax_scaling: bool
    """X offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_x: int
    """Y offset of the layer, in pixels (IMPORTANT: this should be added to the `LayerInstance`
    optional offset)
    """
    px_offset_y: int
    """An array of tags to filter Entities that can be added to this layer"""
    required_tags: List[str]
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_x: float
    """If the tiles are smaller or larger than the layer grid, the pivot value will be used to
    position the tile relatively its grid cell.
    """
    tile_pivot_y: float
    """Type of the layer as Haxe Enum Possible values: `IntGrid`, `Entities`, `Tiles`,
    `AutoLayer`
    """
    layer_definition_type: LayerType
    """Unique Int identifier"""
    uid: int
    auto_source_layer_def_uid: Optional[int] = None
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `tilesetDefUid`
    """
    auto_tileset_def_uid: Optional[int] = None
    """Reference to the default Tileset UID being used by this layer definition.<br/>
    **WARNING**: some layer *instances* might use a different tileset. So most of the time,
    you should probably use the `__tilesetDefUid` value found in layer instances.<br/>  Note:
    since version 1.0.0, the old `autoTilesetDefUid` was removed and merged into this value.
    """
    tileset_def_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "LayerDefinition":
        assert isinstance(obj, dict)
        type = from_str(obj.get("__type"))
        auto_rule_groups = from_list(
            AutoLayerRuleGroup.from_dict, obj.get("autoRuleGroups")
        )
        display_opacity = from_float(obj.get("displayOpacity"))
        excluded_tags = from_list(from_str, obj.get("excludedTags"))
        grid_size = from_int(obj.get("gridSize"))
        guide_grid_hei = from_int(obj.get("guideGridHei"))
        guide_grid_wid = from_int(obj.get("guideGridWid"))
        hide_fields_when_inactive = from_bool(obj.get("hideFieldsWhenInactive"))
        hide_in_list = from_bool(obj.get("hideInList"))
        identifier = from_str(obj.get("identifier"))
        inactive_opacity = from_float(obj.get("inactiveOpacity"))
        int_grid_values = from_list(
            IntGridValueDefinition.from_dict, obj.get("intGridValues")
        )
        parallax_factor_x = from_float(obj.get("parallaxFactorX"))
        parallax_factor_y = from_float(obj.get("parallaxFactorY"))
        parallax_scaling = from_bool(obj.get("parallaxScaling"))
        px_offset_x = from_int(obj.get("pxOffsetX"))
        px_offset_y = from_int(obj.get("pxOffsetY"))
        required_tags = from_list(from_str, obj.get("requiredTags"))
        tile_pivot_x = from_float(obj.get("tilePivotX"))
        tile_pivot_y = from_float(obj.get("tilePivotY"))
        layer_definition_type = LayerType(obj.get("type"))
        uid = from_int(obj.get("uid"))
        auto_source_layer_def_uid = from_union(
            [from_none, from_int], obj.get("autoSourceLayerDefUid")
        )
        auto_tileset_def_uid = from_union(
            [from_none, from_int], obj.get("autoTilesetDefUid")
        )
        tileset_def_uid = from_union([from_none, from_int], obj.get("tilesetDefUid"))
        return LayerDefinition(
            type,
            auto_rule_groups,
            display_opacity,
            excluded_tags,
            grid_size,
            guide_grid_hei,
            guide_grid_wid,
            hide_fields_when_inactive,
            hide_in_list,
            identifier,
            inactive_opacity,
            int_grid_values,
            parallax_factor_x,
            parallax_factor_y,
            parallax_scaling,
            px_offset_x,
            px_offset_y,
            required_tags,
            tile_pivot_x,
            tile_pivot_y,
            layer_definition_type,
            uid,
            auto_source_layer_def_uid,
            auto_tileset_def_uid,
            tileset_def_uid,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__type"] = from_str(self.type)
        result["autoRuleGroups"] = from_list(
            lambda x: to_class(AutoLayerRuleGroup, x), self.auto_rule_groups
        )
        result["displayOpacity"] = to_float(self.display_opacity)
        result["excludedTags"] = from_list(from_str, self.excluded_tags)
        result["gridSize"] = from_int(self.grid_size)
        result["guideGridHei"] = from_int(self.guide_grid_hei)
        result["guideGridWid"] = from_int(self.guide_grid_wid)
        result["hideFieldsWhenInactive"] = from_bool(self.hide_fields_when_inactive)
        result["hideInList"] = from_bool(self.hide_in_list)
        result["identifier"] = from_str(self.identifier)
        result["inactiveOpacity"] = to_float(self.inactive_opacity)
        result["intGridValues"] = from_list(
            lambda x: to_class(IntGridValueDefinition, x), self.int_grid_values
        )
        result["parallaxFactorX"] = to_float(self.parallax_factor_x)
        result["parallaxFactorY"] = to_float(self.parallax_factor_y)
        result["parallaxScaling"] = from_bool(self.parallax_scaling)
        result["pxOffsetX"] = from_int(self.px_offset_x)
        result["pxOffsetY"] = from_int(self.px_offset_y)
        result["requiredTags"] = from_list(from_str, self.required_tags)
        result["tilePivotX"] = to_float(self.tile_pivot_x)
        result["tilePivotY"] = to_float(self.tile_pivot_y)
        result["type"] = to_enum(LayerType, self.layer_definition_type)
        result["uid"] = from_int(self.uid)
        result["autoSourceLayerDefUid"] = from_union(
            [from_none, from_int], self.auto_source_layer_def_uid
        )
        result["autoTilesetDefUid"] = from_union(
            [from_none, from_int], self.auto_tileset_def_uid
        )
        result["tilesetDefUid"] = from_union(
            [from_none, from_int], self.tileset_def_uid
        )
        return result


@dataclass
class TileCustomMetadata:
    """In a tileset definition, user defined meta-data of a tile."""

    data: str
    tile_id: int

    @staticmethod
    def from_dict(obj: Any) -> "TileCustomMetadata":
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        tile_id = from_int(obj.get("tileId"))
        return TileCustomMetadata(data, tile_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["tileId"] = from_int(self.tile_id)
        return result


class EmbedAtlas(Enum):
    LDTK_ICONS = "LdtkIcons"


@dataclass
class EnumTagValue:
    """In a tileset definition, enum based tag infos"""

    enum_value_id: str
    tile_ids: List[int]

    @staticmethod
    def from_dict(obj: Any) -> "EnumTagValue":
        assert isinstance(obj, dict)
        enum_value_id = from_str(obj.get("enumValueId"))
        tile_ids = from_list(from_int, obj.get("tileIds"))
        return EnumTagValue(enum_value_id, tile_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["enumValueId"] = from_str(self.enum_value_id)
        result["tileIds"] = from_list(from_int, self.tile_ids)
        return result


@dataclass
class TilesetDefinition:
    """The `Tileset` definition is the most important part among project definitions. It
    contains some extra informations about each integrated tileset. If you only had to parse
    one definition section, that would be the one.
    """

    """Grid-based height"""
    c_hei: int
    """Grid-based width"""
    c_wid: int
    """An array of custom tile metadata"""
    custom_data: List[TileCustomMetadata]
    """Tileset tags using Enum values specified by `tagsSourceEnumId`. This array contains 1
    element per Enum value, which contains an array of all Tile IDs that are tagged with it.
    """
    enum_tags: List[EnumTagValue]
    """User defined unique identifier"""
    identifier: str
    """Distance in pixels from image borders"""
    padding: int
    """Image height in pixels"""
    px_hei: int
    """Image width in pixels"""
    px_wid: int
    """Path to the source file, relative to the current project JSON file"""
    rel_path: str
    """Array of group of tiles selections, only meant to be used in the editor"""
    saved_selections: List[Dict[str, Any]]
    """Space in pixels between all tiles"""
    spacing: int
    """An array of user-defined tags to organize the Tilesets"""
    tags: List[str]
    tile_grid_size: int
    """Unique Intidentifier"""
    uid: int
    """The following data is used internally for various optimizations. It's always synced with
    source image changes.
    """
    cached_pixel_data: Optional[Dict[str, Any]] = None
    """If this value is set, then it means that this atlas uses an internal LDtk atlas image
    instead of a loaded one. Possible values: &lt;`null`&gt;, `LdtkIcons`
    """
    embed_atlas: Optional[EmbedAtlas] = None
    """Optional Enum definition UID used for this tileset meta-data"""
    tags_source_enum_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TilesetDefinition":
        assert isinstance(obj, dict)
        c_hei = from_int(obj.get("__cHei"))
        c_wid = from_int(obj.get("__cWid"))
        custom_data = from_list(TileCustomMetadata.from_dict, obj.get("customData"))
        enum_tags = from_list(EnumTagValue.from_dict, obj.get("enumTags"))
        identifier = from_str(obj.get("identifier"))
        padding = from_int(obj.get("padding"))
        px_hei = from_int(obj.get("pxHei"))
        px_wid = from_int(obj.get("pxWid"))
        rel_path = from_str(obj.get("relPath"))
        saved_selections = from_list(
            lambda x: from_dict(lambda x: x, x), obj.get("savedSelections")
        )
        spacing = from_int(obj.get("spacing"))
        tags = from_list(from_str, obj.get("tags"))
        tile_grid_size = from_int(obj.get("tileGridSize"))
        uid = from_int(obj.get("uid"))
        cached_pixel_data = from_union(
            [from_none, lambda x: from_dict(lambda x: x, x)], obj.get("cachedPixelData")
        )
        embed_atlas = from_union([from_none, EmbedAtlas], obj.get("embedAtlas"))
        tags_source_enum_uid = from_union(
            [from_none, from_int], obj.get("tagsSourceEnumUid")
        )
        return TilesetDefinition(
            c_hei,
            c_wid,
            custom_data,
            enum_tags,
            identifier,
            padding,
            px_hei,
            px_wid,
            rel_path,
            saved_selections,
            spacing,
            tags,
            tile_grid_size,
            uid,
            cached_pixel_data,
            embed_atlas,
            tags_source_enum_uid,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_int(self.c_hei)
        result["__cWid"] = from_int(self.c_wid)
        result["customData"] = from_list(
            lambda x: to_class(TileCustomMetadata, x), self.custom_data
        )
        result["enumTags"] = from_list(
            lambda x: to_class(EnumTagValue, x), self.enum_tags
        )
        result["identifier"] = from_str(self.identifier)
        result["padding"] = from_int(self.padding)
        result["pxHei"] = from_int(self.px_hei)
        result["pxWid"] = from_int(self.px_wid)
        result["relPath"] = from_str(self.rel_path)
        result["savedSelections"] = from_list(
            lambda x: from_dict(lambda x: x, x), self.saved_selections
        )
        result["spacing"] = from_int(self.spacing)
        result["tags"] = from_list(from_str, self.tags)
        result["tileGridSize"] = from_int(self.tile_grid_size)
        result["uid"] = from_int(self.uid)
        result["cachedPixelData"] = from_union(
            [from_none, lambda x: from_dict(lambda x: x, x)], self.cached_pixel_data
        )
        result["embedAtlas"] = from_union(
            [from_none, lambda x: to_enum(EmbedAtlas, x)], self.embed_atlas
        )
        result["tagsSourceEnumUid"] = from_union(
            [from_none, from_int], self.tags_source_enum_uid
        )
        return result


@dataclass
class Definitions:
    """A structure containing all the definitions of this project
    
    If you're writing your own LDtk importer, you should probably just ignore *most* stuff in
    the `defs` section, as it contains data that are mostly important to the editor. To keep
    you away from the `defs` section and avoid some unnecessary JSON parsing, important data
    from definitions is often duplicated in fields prefixed with a double underscore (eg.
    `__identifier` or `__type`).  The 2 only definition types you might need here are
    **Tilesets** and **Enums**.
    """

    """All entities definitions, including their custom fields"""
    entities: List[EntityDefinition]
    """All internal enums"""
    enums: List[EnumDefinition]
    """Note: external enums are exactly the same as `enums`, except they have a `relPath` to
    point to an external source file.
    """
    external_enums: List[EnumDefinition]
    """All layer definitions"""
    layers: List[LayerDefinition]
    """All custom fields available to all levels."""
    level_fields: List[FieldDefinition]
    """All tilesets"""
    tilesets: List[TilesetDefinition]

    @staticmethod
    def from_dict(obj: Any) -> "Definitions":
        assert isinstance(obj, dict)
        entities = from_list(EntityDefinition.from_dict, obj.get("entities"))
        enums = from_list(EnumDefinition.from_dict, obj.get("enums"))
        external_enums = from_list(EnumDefinition.from_dict, obj.get("externalEnums"))
        layers = from_list(LayerDefinition.from_dict, obj.get("layers"))
        level_fields = from_list(FieldDefinition.from_dict, obj.get("levelFields"))
        tilesets = from_list(TilesetDefinition.from_dict, obj.get("tilesets"))
        return Definitions(
            entities, enums, external_enums, layers, level_fields, tilesets
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["entities"] = from_list(
            lambda x: to_class(EntityDefinition, x), self.entities
        )
        result["enums"] = from_list(lambda x: to_class(EnumDefinition, x), self.enums)
        result["externalEnums"] = from_list(
            lambda x: to_class(EnumDefinition, x), self.external_enums
        )
        result["layers"] = from_list(
            lambda x: to_class(LayerDefinition, x), self.layers
        )
        result["levelFields"] = from_list(
            lambda x: to_class(FieldDefinition, x), self.level_fields
        )
        result["tilesets"] = from_list(
            lambda x: to_class(TilesetDefinition, x), self.tilesets
        )
        return result


class Flag(Enum):
    EXPORT_PRE_CSV_INT_GRID_FORMAT = "ExportPreCsvIntGridFormat"
    IGNORE_BACKUP_SUGGEST = "IgnoreBackupSuggest"
    MULTI_WORLDS = "MultiWorlds"
    PREPEND_INDEX_TO_LEVEL_FILE_NAMES = "PrependIndexToLevelFileNames"
    USE_MULTILINES_TYPE = "UseMultilinesType"


class IdentifierStyle(Enum):
    """Naming convention for Identifiers (first-letter uppercase, full uppercase etc.) Possible
    values: `Capitalize`, `Uppercase`, `Lowercase`, `Free`
    """

    CAPITALIZE = "Capitalize"
    FREE = "Free"
    LOWERCASE = "Lowercase"
    UPPERCASE = "Uppercase"


class ImageExportMode(Enum):
    """"Image export" option when saving project. Possible values: `None`, `OneImagePerLayer`,
    `OneImagePerLevel`
    """

    NONE = "None"
    ONE_IMAGE_PER_LAYER = "OneImagePerLayer"
    ONE_IMAGE_PER_LEVEL = "OneImagePerLevel"


@dataclass
class LevelBackgroundPosition:
    """Level background image position info"""

    """An array of 4 float values describing the cropped sub-rectangle of the displayed
    background image. This cropping happens when original is larger than the level bounds.
    Array format: `[ cropX, cropY, cropWidth, cropHeight ]`
    """
    crop_rect: List[float]
    """An array containing the `[scaleX,scaleY]` values of the **cropped** background image,
    depending on `bgPos` option.
    """
    scale: List[float]
    """An array containing the `[x,y]` pixel coordinates of the top-left corner of the
    **cropped** background image, depending on `bgPos` option.
    """
    top_left_px: List[int]

    @staticmethod
    def from_dict(obj: Any) -> "LevelBackgroundPosition":
        assert isinstance(obj, dict)
        crop_rect = from_list(from_float, obj.get("cropRect"))
        scale = from_list(from_float, obj.get("scale"))
        top_left_px = from_list(from_int, obj.get("topLeftPx"))
        return LevelBackgroundPosition(crop_rect, scale, top_left_px)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cropRect"] = from_list(to_float, self.crop_rect)
        result["scale"] = from_list(to_float, self.scale)
        result["topLeftPx"] = from_list(from_int, self.top_left_px)
        return result


@dataclass
class FieldInstance:
    """Field definition identifier"""

    identifier: str
    """Type of the field, such as `Int`, `Float`, `String`, `Enum(my_enum_name)`, `Bool`,
    etc.<br/>  NOTE: if you enable the advanced option **Use Multilines type**, you will have
    "*Multilines*" instead of "*String*" when relevant.
    """
    type: str
    """Actual value of the field instance. The value type varies, depending on `__type`:<br/>
    - For **classic types** (ie. Integer, Float, Boolean, String, Text and FilePath), you
    just get the actual value with the expected type.<br/>   - For **Color**, the value is an
    hexadecimal string using "#rrggbb" format.<br/>   - For **Enum**, the value is a String
    representing the selected enum value.<br/>   - For **Point**, the value is a
    [GridPoint](#ldtk-GridPoint) object.<br/>   - For **Tile**, the value is a
    [TilesetRect](#ldtk-TilesetRect) object.<br/>   - For **EntityRef**, the value is an
    [EntityReferenceInfos](#ldtk-EntityReferenceInfos) object.<br/><br/>  If the field is an
    array, then this `__value` will also be a JSON array.
    """
    value: Any
    """Reference of the **Field definition** UID"""
    def_uid: int
    """Editor internal raw values"""
    real_editor_values: List[Any]
    """Optional TilesetRect used to display this field (this can be the field own Tile, or some
    other Tile guessed from the value, like an Enum).
    """
    tile: Optional[TilesetRectangle] = None

    @staticmethod
    def from_dict(obj: Any) -> "FieldInstance":
        assert isinstance(obj, dict)
        identifier = from_str(obj.get("__identifier"))
        type = from_str(obj.get("__type"))
        value = obj.get("__value")
        def_uid = from_int(obj.get("defUid"))
        real_editor_values = from_list(lambda x: x, obj.get("realEditorValues"))
        tile = from_union([from_none, TilesetRectangle.from_dict], obj.get("__tile"))
        return FieldInstance(identifier, type, value, def_uid, real_editor_values, tile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__identifier"] = from_str(self.identifier)
        result["__type"] = from_str(self.type)
        result["__value"] = self.value
        result["defUid"] = from_int(self.def_uid)
        result["realEditorValues"] = from_list(lambda x: x, self.real_editor_values)
        result["__tile"] = from_union(
            [from_none, lambda x: to_class(TilesetRectangle, x)], self.tile
        )
        return result


@dataclass
class TileInstance:
    """This structure represents a single tile from a given Tileset."""

    """Internal data used by the editor.<br/>  For auto-layer tiles: `[ruleId, coordId]`.<br/>
    For tile-layer tiles: `[coordId]`.
    """
    d: List[int]
    """"Flip bits", a 2-bits integer to represent the mirror transformations of the tile.<br/>
    - Bit 0 = X flip<br/>   - Bit 1 = Y flip<br/>   Examples: f=0 (no flip), f=1 (X flip
    only), f=2 (Y flip only), f=3 (both flips)
    """
    f: int
    """Pixel coordinates of the tile in the **layer** (`[x,y]` format). Don't forget optional
    layer offsets, if they exist!
    """
    px: List[int]
    """Pixel coordinates of the tile in the **tileset** (`[x,y]` format)"""
    src: List[int]
    """The *Tile ID* in the corresponding tileset."""
    t: int

    @staticmethod
    def from_dict(obj: Any) -> "TileInstance":
        assert isinstance(obj, dict)
        d = from_list(from_int, obj.get("d"))
        f = from_int(obj.get("f"))
        px = from_list(from_int, obj.get("px"))
        src = from_list(from_int, obj.get("src"))
        t = from_int(obj.get("t"))
        return TileInstance(d, f, px, src, t)

    def to_dict(self) -> dict:
        result: dict = {}
        result["d"] = from_list(from_int, self.d)
        result["f"] = from_int(self.f)
        result["px"] = from_list(from_int, self.px)
        result["src"] = from_list(from_int, self.src)
        result["t"] = from_int(self.t)
        return result


@dataclass
class EntityInstance:
    """Grid-based coordinates (`[x,y]` format)"""

    grid: List[int]
    """Entity definition identifier"""
    identifier: str
    """Pivot coordinates  (`[x,y]` format, values are from 0 to 1) of the Entity"""
    pivot: List[float]
    """The entity "smart" color, guessed from either Entity definition, or one its field
    instances.
    """
    smart_color: str
    """Array of tags defined in this Entity definition"""
    tags: List[str]
    """Reference of the **Entity definition** UID"""
    def_uid: int
    """An array of all custom fields and their values."""
    field_instances: List[FieldInstance]
    """Entity height in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    height: int
    """Unique instance identifier"""
    iid: str
    """Pixel coordinates (`[x,y]` format) in current level coordinate space. Don't forget
    optional layer offsets, if they exist!
    """
    px: List[int]
    """Entity width in pixels. For non-resizable entities, it will be the same as Entity
    definition.
    """
    width: int
    """Optional TilesetRect used to display this entity (it could either be the default Entity
    tile, or some tile provided by a field value, like an Enum).
    """
    tile: Optional[TilesetRectangle] = None

    @staticmethod
    def from_dict(obj: Any) -> "EntityInstance":
        assert isinstance(obj, dict)
        grid = from_list(from_int, obj.get("__grid"))
        identifier = from_str(obj.get("__identifier"))
        pivot = from_list(from_float, obj.get("__pivot"))
        smart_color = from_str(obj.get("__smartColor"))
        tags = from_list(from_str, obj.get("__tags"))
        def_uid = from_int(obj.get("defUid"))
        field_instances = from_list(FieldInstance.from_dict, obj.get("fieldInstances"))
        height = from_int(obj.get("height"))
        iid = from_str(obj.get("iid"))
        px = from_list(from_int, obj.get("px"))
        width = from_int(obj.get("width"))
        tile = from_union([from_none, TilesetRectangle.from_dict], obj.get("__tile"))
        return EntityInstance(
            grid,
            identifier,
            pivot,
            smart_color,
            tags,
            def_uid,
            field_instances,
            height,
            iid,
            px,
            width,
            tile,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__grid"] = from_list(from_int, self.grid)
        result["__identifier"] = from_str(self.identifier)
        result["__pivot"] = from_list(to_float, self.pivot)
        result["__smartColor"] = from_str(self.smart_color)
        result["__tags"] = from_list(from_str, self.tags)
        result["defUid"] = from_int(self.def_uid)
        result["fieldInstances"] = from_list(
            lambda x: to_class(FieldInstance, x), self.field_instances
        )
        result["height"] = from_int(self.height)
        result["iid"] = from_str(self.iid)
        result["px"] = from_list(from_int, self.px)
        result["width"] = from_int(self.width)
        result["__tile"] = from_union(
            [from_none, lambda x: to_class(TilesetRectangle, x)], self.tile
        )
        return result


@dataclass
class IntGridValueInstance:
    """IntGrid value instance"""

    """Coordinate ID in the layer grid"""
    coord_id: int
    """IntGrid value"""
    v: int

    @staticmethod
    def from_dict(obj: Any) -> "IntGridValueInstance":
        assert isinstance(obj, dict)
        coord_id = from_int(obj.get("coordId"))
        v = from_int(obj.get("v"))
        return IntGridValueInstance(coord_id, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordId"] = from_int(self.coord_id)
        result["v"] = from_int(self.v)
        return result


@dataclass
class LayerInstance:
    """Grid-based height"""

    c_hei: int
    """Grid-based width"""
    c_wid: int
    """Grid size"""
    grid_size: int
    """Layer definition identifier"""
    identifier: str
    """Layer opacity as Float [0-1]"""
    opacity: float
    """Total layer X pixel offset, including both instance and definition offsets."""
    px_total_offset_x: int
    """Total layer Y pixel offset, including both instance and definition offsets."""
    px_total_offset_y: int
    """Layer type (possible values: IntGrid, Entities, Tiles or AutoLayer)"""
    type: str
    """An array containing all tiles generated by Auto-layer rules. The array is already sorted
    in display order (ie. 1st tile is beneath 2nd, which is beneath 3rd etc.).<br/><br/>
    Note: if multiple tiles are stacked in the same cell as the result of different rules,
    all tiles behind opaque ones will be discarded.
    """
    auto_layer_tiles: List[TileInstance]
    entity_instances: List[EntityInstance]
    grid_tiles: List[TileInstance]
    """Unique layer instance identifier"""
    iid: str
    """A list of all values in the IntGrid layer, stored in CSV format (Comma Separated
    Values).<br/>  Order is from left to right, and top to bottom (ie. first row from left to
    right, followed by second row, etc).<br/>  `0` means "empty cell" and IntGrid values
    start at 1.<br/>  The array size is `__cWid` x `__cHei` cells.
    """
    int_grid_csv: List[int]
    """Reference the Layer definition UID"""
    layer_def_uid: int
    """Reference to the UID of the level containing this layer instance"""
    level_id: int
    """An Array containing the UIDs of optional rules that were enabled in this specific layer
    instance.
    """
    optional_rules: List[int]
    """X offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetX`)
    """
    px_offset_x: int
    """Y offset in pixels to render this layer, usually 0 (IMPORTANT: this should be added to
    the `LayerDef` optional offset, see `__pxTotalOffsetY`)
    """
    px_offset_y: int
    """Random seed used for Auto-Layers rendering"""
    seed: int
    """Layer instance visibility"""
    visible: bool
    """The definition UID of corresponding Tileset, if any."""
    tileset_def_uid: Optional[int] = None
    """The relative path to corresponding Tileset, if any."""
    tileset_rel_path: Optional[str] = None
    """**WARNING**: this deprecated value will be *removed* completely on version 1.0.0+
    Replaced by: `intGridCsv`
    """
    int_grid: Optional[List[IntGridValueInstance]] = None
    """This layer can use another tileset by overriding the tileset UID here."""
    override_tileset_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "LayerInstance":
        assert isinstance(obj, dict)
        c_hei = from_int(obj.get("__cHei"))
        c_wid = from_int(obj.get("__cWid"))
        grid_size = from_int(obj.get("__gridSize"))
        identifier = from_str(obj.get("__identifier"))
        opacity = from_float(obj.get("__opacity"))
        px_total_offset_x = from_int(obj.get("__pxTotalOffsetX"))
        px_total_offset_y = from_int(obj.get("__pxTotalOffsetY"))
        type = from_str(obj.get("__type"))
        auto_layer_tiles = from_list(TileInstance.from_dict, obj.get("autoLayerTiles"))
        entity_instances = from_list(
            EntityInstance.from_dict, obj.get("entityInstances")
        )
        grid_tiles = from_list(TileInstance.from_dict, obj.get("gridTiles"))
        iid = from_str(obj.get("iid"))
        int_grid_csv = from_list(from_int, obj.get("intGridCsv"))
        layer_def_uid = from_int(obj.get("layerDefUid"))
        level_id = from_int(obj.get("levelId"))
        optional_rules = from_list(from_int, obj.get("optionalRules"))
        px_offset_x = from_int(obj.get("pxOffsetX"))
        px_offset_y = from_int(obj.get("pxOffsetY"))
        seed = from_int(obj.get("seed"))
        visible = from_bool(obj.get("visible"))
        tileset_def_uid = from_union([from_none, from_int], obj.get("__tilesetDefUid"))
        tileset_rel_path = from_union(
            [from_none, from_str], obj.get("__tilesetRelPath")
        )
        int_grid = from_union(
            [from_none, lambda x: from_list(IntGridValueInstance.from_dict, x)],
            obj.get("intGrid"),
        )
        override_tileset_uid = from_union(
            [from_none, from_int], obj.get("overrideTilesetUid")
        )
        return LayerInstance(
            c_hei,
            c_wid,
            grid_size,
            identifier,
            opacity,
            px_total_offset_x,
            px_total_offset_y,
            type,
            auto_layer_tiles,
            entity_instances,
            grid_tiles,
            iid,
            int_grid_csv,
            layer_def_uid,
            level_id,
            optional_rules,
            px_offset_x,
            px_offset_y,
            seed,
            visible,
            tileset_def_uid,
            tileset_rel_path,
            int_grid,
            override_tileset_uid,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__cHei"] = from_int(self.c_hei)
        result["__cWid"] = from_int(self.c_wid)
        result["__gridSize"] = from_int(self.grid_size)
        result["__identifier"] = from_str(self.identifier)
        result["__opacity"] = to_float(self.opacity)
        result["__pxTotalOffsetX"] = from_int(self.px_total_offset_x)
        result["__pxTotalOffsetY"] = from_int(self.px_total_offset_y)
        result["__type"] = from_str(self.type)
        result["autoLayerTiles"] = from_list(
            lambda x: to_class(TileInstance, x), self.auto_layer_tiles
        )
        result["entityInstances"] = from_list(
            lambda x: to_class(EntityInstance, x), self.entity_instances
        )
        result["gridTiles"] = from_list(
            lambda x: to_class(TileInstance, x), self.grid_tiles
        )
        result["iid"] = from_str(self.iid)
        result["intGridCsv"] = from_list(from_int, self.int_grid_csv)
        result["layerDefUid"] = from_int(self.layer_def_uid)
        result["levelId"] = from_int(self.level_id)
        result["optionalRules"] = from_list(from_int, self.optional_rules)
        result["pxOffsetX"] = from_int(self.px_offset_x)
        result["pxOffsetY"] = from_int(self.px_offset_y)
        result["seed"] = from_int(self.seed)
        result["visible"] = from_bool(self.visible)
        result["__tilesetDefUid"] = from_union(
            [from_none, from_int], self.tileset_def_uid
        )
        result["__tilesetRelPath"] = from_union(
            [from_none, from_str], self.tileset_rel_path
        )
        result["intGrid"] = from_union(
            [
                from_none,
                lambda x: from_list(lambda x: to_class(IntGridValueInstance, x), x),
            ],
            self.int_grid,
        )
        result["overrideTilesetUid"] = from_union(
            [from_none, from_int], self.override_tileset_uid
        )
        return result


class BgPos(Enum):
    CONTAIN = "Contain"
    COVER = "Cover"
    COVER_DIRTY = "CoverDirty"
    UNSCALED = "Unscaled"


@dataclass
class NeighbourLevel:
    """Nearby level info"""

    """A single lowercase character tipping on the level location (`n`orth, `s`outh, `w`est,
    `e`ast).
    """
    dir: str
    """Neighbour Instance Identifier"""
    level_iid: str
    """**WARNING**: this deprecated value will be *removed* completely on version 1.2.0+
    Replaced by: `levelIid`
    """
    level_uid: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "NeighbourLevel":
        assert isinstance(obj, dict)
        dir = from_str(obj.get("dir"))
        level_iid = from_str(obj.get("levelIid"))
        level_uid = from_union([from_none, from_int], obj.get("levelUid"))
        return NeighbourLevel(dir, level_iid, level_uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dir"] = from_str(self.dir)
        result["levelIid"] = from_str(self.level_iid)
        result["levelUid"] = from_union([from_none, from_int], self.level_uid)
        return result


@dataclass
class Level:
    """This section contains all the level data. It can be found in 2 distinct forms, depending
    on Project current settings:  - If "*Separate level files*" is **disabled** (default):
    full level data is *embedded* inside the main Project JSON file, - If "*Separate level
    files*" is **enabled**: level data is stored in *separate* standalone `.ldtkl` files (one
    per level). In this case, the main Project JSON file will still contain most level data,
    except heavy sections, like the `layerInstances` array (which will be null). The
    `externalRelPath` string points to the `ldtkl` file.  A `ldtkl` file is just a JSON file
    containing exactly what is described below.
    """

    """Background color of the level (same as `bgColor`, except the default value is
    automatically used here if its value is `null`)
    """
    bg_color: str
    """An array listing all other levels touching this one on the world map.<br/>  Only relevant
    for world layouts where level spatial positioning is manual (ie. GridVania, Free). For
    Horizontal and Vertical layouts, this array is always empty.
    """
    neighbours: List[NeighbourLevel]
    """The "guessed" color for this level in the editor, decided using either the background
    color or an existing custom field.
    """
    smart_color: str
    """Background image X pivot (0-1)"""
    bg_pivot_x: float
    """Background image Y pivot (0-1)"""
    bg_pivot_y: float
    """An array containing this level custom field values."""
    field_instances: List[FieldInstance]
    """User defined unique identifier"""
    identifier: str
    """Unique instance identifier"""
    iid: str
    """Height of the level in pixels"""
    px_hei: int
    """Width of the level in pixels"""
    px_wid: int
    """Unique Int identifier"""
    uid: int
    """If TRUE, the level identifier will always automatically use the naming pattern as defined
    in `Project.levelNamePattern`. Becomes FALSE if the identifier is manually modified by
    user.
    """
    use_auto_identifier: bool
    """Index that represents the "depth" of the level in the world. Default is 0, greater means
    "above", lower means "below".<br/>  This value is mostly used for display only and is
    intended to make stacking of levels easier to manage.
    """
    world_depth: int
    """World X coordinate in pixels.<br/>  Only relevant for world layouts where level spatial
    positioning is manual (ie. GridVania, Free). For Horizontal and Vertical layouts, the
    value is always -1 here.
    """
    world_x: int
    """World Y coordinate in pixels.<br/>  Only relevant for world layouts where level spatial
    positioning is manual (ie. GridVania, Free). For Horizontal and Vertical layouts, the
    value is always -1 here.
    """
    world_y: int
    """Position informations of the background image, if there is one."""
    bg_pos: Optional[LevelBackgroundPosition] = None
    """Background color of the level. If `null`, the project `defaultLevelBgColor` should be
    used.
    """
    level_bg_color: Optional[str] = None
    """An enum defining the way the background image (if any) is positioned on the level. See
    `__bgPos` for resulting position info. Possible values: &lt;`null`&gt;, `Unscaled`,
    `Contain`, `Cover`, `CoverDirty`
    """
    level_bg_pos: Optional[BgPos] = None
    """The *optional* relative path to the level background image."""
    bg_rel_path: Optional[str] = None
    """This value is not null if the project option "*Save levels separately*" is enabled. In
    this case, this **relative** path points to the level Json file.
    """
    external_rel_path: Optional[str] = None
    """An array containing all Layer instances. **IMPORTANT**: if the project option "*Save
    levels separately*" is enabled, this field will be `null`.<br/>  This array is **sorted
    in display order**: the 1st layer is the top-most and the last is behind.
    """
    layer_instances: Optional[List[LayerInstance]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Level":
        assert isinstance(obj, dict)
        bg_color = from_str(obj.get("__bgColor"))
        neighbours = from_list(NeighbourLevel.from_dict, obj.get("__neighbours"))
        smart_color = from_str(obj.get("__smartColor"))
        bg_pivot_x = from_float(obj.get("bgPivotX"))
        bg_pivot_y = from_float(obj.get("bgPivotY"))
        field_instances = from_list(FieldInstance.from_dict, obj.get("fieldInstances"))
        identifier = from_str(obj.get("identifier"))
        iid = from_str(obj.get("iid"))
        px_hei = from_int(obj.get("pxHei"))
        px_wid = from_int(obj.get("pxWid"))
        uid = from_int(obj.get("uid"))
        use_auto_identifier = from_bool(obj.get("useAutoIdentifier"))
        world_depth = from_int(obj.get("worldDepth"))
        world_x = from_int(obj.get("worldX"))
        world_y = from_int(obj.get("worldY"))
        bg_pos = from_union(
            [from_none, LevelBackgroundPosition.from_dict], obj.get("__bgPos")
        )
        level_bg_color = from_union([from_none, from_str], obj.get("bgColor"))
        level_bg_pos = from_union([from_none, BgPos], obj.get("bgPos"))
        bg_rel_path = from_union([from_none, from_str], obj.get("bgRelPath"))
        external_rel_path = from_union(
            [from_none, from_str], obj.get("externalRelPath")
        )
        layer_instances = from_union(
            [from_none, lambda x: from_list(LayerInstance.from_dict, x)],
            obj.get("layerInstances"),
        )
        return Level(
            bg_color,
            neighbours,
            smart_color,
            bg_pivot_x,
            bg_pivot_y,
            field_instances,
            identifier,
            iid,
            px_hei,
            px_wid,
            uid,
            use_auto_identifier,
            world_depth,
            world_x,
            world_y,
            bg_pos,
            level_bg_color,
            level_bg_pos,
            bg_rel_path,
            external_rel_path,
            layer_instances,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["__bgColor"] = from_str(self.bg_color)
        result["__neighbours"] = from_list(
            lambda x: to_class(NeighbourLevel, x), self.neighbours
        )
        result["__smartColor"] = from_str(self.smart_color)
        result["bgPivotX"] = to_float(self.bg_pivot_x)
        result["bgPivotY"] = to_float(self.bg_pivot_y)
        result["fieldInstances"] = from_list(
            lambda x: to_class(FieldInstance, x), self.field_instances
        )
        result["identifier"] = from_str(self.identifier)
        result["iid"] = from_str(self.iid)
        result["pxHei"] = from_int(self.px_hei)
        result["pxWid"] = from_int(self.px_wid)
        result["uid"] = from_int(self.uid)
        result["useAutoIdentifier"] = from_bool(self.use_auto_identifier)
        result["worldDepth"] = from_int(self.world_depth)
        result["worldX"] = from_int(self.world_x)
        result["worldY"] = from_int(self.world_y)
        result["__bgPos"] = from_union(
            [from_none, lambda x: to_class(LevelBackgroundPosition, x)], self.bg_pos
        )
        result["bgColor"] = from_union([from_none, from_str], self.level_bg_color)
        result["bgPos"] = from_union(
            [from_none, lambda x: to_enum(BgPos, x)], self.level_bg_pos
        )
        result["bgRelPath"] = from_union([from_none, from_str], self.bg_rel_path)
        result["externalRelPath"] = from_union(
            [from_none, from_str], self.external_rel_path
        )
        result["layerInstances"] = from_union(
            [from_none, lambda x: from_list(lambda x: to_class(LayerInstance, x), x)],
            self.layer_instances,
        )
        return result


class WorldLayout(Enum):
    FREE = "Free"
    GRID_VANIA = "GridVania"
    LINEAR_HORIZONTAL = "LinearHorizontal"
    LINEAR_VERTICAL = "LinearVertical"


@dataclass
class World:
    """**IMPORTANT**: this type is not used *yet* in current LDtk version. It's only presented
    here as a preview of a planned feature.  A World contains multiple levels, and it has its
    own layout settings.
    """

    """Default new level height"""
    default_level_height: int
    """Default new level width"""
    default_level_width: int
    """User defined unique identifier"""
    identifier: str
    """Unique instance identifer"""
    iid: str
    """All levels from this world. The order of this array is only relevant in
    `LinearHorizontal` and `linearVertical` world layouts (see `worldLayout` value).
    Otherwise, you should refer to the `worldX`,`worldY` coordinates of each Level.
    """
    levels: List[Level]
    """Height of the world grid in pixels."""
    world_grid_height: int
    """Width of the world grid in pixels."""
    world_grid_width: int
    """An enum that describes how levels are organized in this project (ie. linearly or in a 2D
    space). Possible values: `Free`, `GridVania`, `LinearHorizontal`, `LinearVertical`, `null`
    """
    world_layout: Optional[WorldLayout] = None

    @staticmethod
    def from_dict(obj: Any) -> "World":
        assert isinstance(obj, dict)
        default_level_height = from_int(obj.get("defaultLevelHeight"))
        default_level_width = from_int(obj.get("defaultLevelWidth"))
        identifier = from_str(obj.get("identifier"))
        iid = from_str(obj.get("iid"))
        levels = from_list(Level.from_dict, obj.get("levels"))
        world_grid_height = from_int(obj.get("worldGridHeight"))
        world_grid_width = from_int(obj.get("worldGridWidth"))
        world_layout = from_union([from_none, WorldLayout], obj.get("worldLayout"))
        return World(
            default_level_height,
            default_level_width,
            identifier,
            iid,
            levels,
            world_grid_height,
            world_grid_width,
            world_layout,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["defaultLevelHeight"] = from_int(self.default_level_height)
        result["defaultLevelWidth"] = from_int(self.default_level_width)
        result["identifier"] = from_str(self.identifier)
        result["iid"] = from_str(self.iid)
        result["levels"] = from_list(lambda x: to_class(Level, x), self.levels)
        result["worldGridHeight"] = from_int(self.world_grid_height)
        result["worldGridWidth"] = from_int(self.world_grid_width)
        result["worldLayout"] = from_union(
            [from_none, lambda x: to_enum(WorldLayout, x)], self.world_layout
        )
        return result


@dataclass
class LdtkJSON:
    """This file is a JSON schema of files created by LDtk level editor (https://ldtk.io).
    
    This is the root of any Project JSON file. It contains:  - the project settings, - an
    array of levels, - a group of definitions (that can probably be safely ignored for most
    users).
    """

    """LDtk application build identifier.<br/>  This is only used to identify the LDtk version
    that generated this particular project file, which can be useful for specific bug fixing.
    Note that the build identifier is just the date of the release, so it's not unique to
    each user (one single global ID per LDtk public release), and as a result, completely
    anonymous.
    """
    app_build_id: float
    """Number of backup files to keep, if the `backupOnSave` is TRUE"""
    backup_limit: int
    """If TRUE, an extra copy of the project will be created in a sub folder, when saving."""
    backup_on_save: bool
    """Project background color"""
    bg_color: str
    """Default grid size for new layers"""
    default_grid_size: int
    """Default background color of levels"""
    default_level_bg_color: str
    """Default X pivot (0 to 1) for new entities"""
    default_pivot_x: float
    """Default Y pivot (0 to 1) for new entities"""
    default_pivot_y: float
    """A structure containing all the definitions of this project"""
    defs: Definitions
    """If TRUE, a Tiled compatible file will also be generated along with the LDtk JSON file
    (default is FALSE)
    """
    export_tiled: bool
    """If TRUE, one file will be saved for the project (incl. all its definitions) and one file
    in a sub-folder for each level.
    """
    external_levels: bool
    """An array containing various advanced flags (ie. options or other states). Possible
    values: `ExportPreCsvIntGridFormat`, `IgnoreBackupSuggest`,
    `PrependIndexToLevelFileNames`, `MultiWorlds`, `UseMultilinesType`
    """
    flags: List[Flag]
    """Naming convention for Identifiers (first-letter uppercase, full uppercase etc.) Possible
    values: `Capitalize`, `Uppercase`, `Lowercase`, `Free`
    """
    identifier_style: IdentifierStyle
    """"Image export" option when saving project. Possible values: `None`, `OneImagePerLayer`,
    `OneImagePerLevel`
    """
    image_export_mode: ImageExportMode
    """File format version"""
    json_version: str
    """The default naming convention for level identifiers."""
    level_name_pattern: str
    """All levels. The order of this array is only relevant in `LinearHorizontal` and
    `linearVertical` world layouts (see `worldLayout` value).<br/>  Otherwise, you should
    refer to the `worldX`,`worldY` coordinates of each Level.
    """
    levels: List[Level]
    """If TRUE, the Json is partially minified (no indentation, nor line breaks, default is
    FALSE)
    """
    minify_json: bool
    """Next Unique integer ID available"""
    next_uid: int
    """This array is not used yet in current LDtk version (so, for now, it's always
    empty).<br/><br/>In a later update, it will be possible to have multiple Worlds in a
    single project, each containing multiple Levels.<br/><br/>What will change when "Multiple
    worlds" support will be added to LDtk:<br/><br/> - in current version, a LDtk project
    file can only contain a single world with multiple levels in it. In this case, levels and
    world layout related settings are stored in the root of the JSON.<br/> - after the
    "Multiple worlds" update, there will be a `worlds` array in root, each world containing
    levels and layout settings. Basically, it's pretty much only about moving the `levels`
    array to the `worlds` array, along with world layout related values (eg. `worldGridWidth`
    etc).<br/><br/>If you want to start supporting this future update easily, please refer to
    this documentation: https://github.com/deepnight/ldtk/issues/231
    """
    worlds: List[World]
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Default new level height
    """
    default_level_height: Optional[int] = None
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Default new level width
    """
    default_level_width: Optional[int] = None
    """**WARNING**: this deprecated value is no longer exported since version 0.9.3  Replaced
    by: `imageExportMode`
    """
    export_png: Optional[bool] = None
    """File naming pattern for exported PNGs"""
    png_file_pattern: Optional[str] = None
    """This optional description is used by LDtk Samples to show up some informations and
    instructions.
    """
    tutorial_desc: Optional[str] = None
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Height of the world grid in pixels.
    """
    world_grid_height: Optional[int] = None
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  Width of the world grid in pixels.
    """
    world_grid_width: Optional[int] = None
    """**WARNING**: this field will move to the `worlds` array after the "multi-worlds" update.
    It will then be `null`. You can enable the Multi-worlds advanced project option to enable
    the change immediately.<br/><br/>  An enum that describes how levels are organized in
    this project (ie. linearly or in a 2D space). Possible values: &lt;`null`&gt;, `Free`,
    `GridVania`, `LinearHorizontal`, `LinearVertical`
    """
    world_layout: Optional[WorldLayout] = None

    @staticmethod
    def from_dict(obj: Any) -> "LdtkJSON":
        assert isinstance(obj, dict)
        app_build_id = from_float(obj.get("appBuildId"))
        backup_limit = from_int(obj.get("backupLimit"))
        backup_on_save = from_bool(obj.get("backupOnSave"))
        bg_color = from_str(obj.get("bgColor"))
        default_grid_size = from_int(obj.get("defaultGridSize"))
        default_level_bg_color = from_str(obj.get("defaultLevelBgColor"))
        default_pivot_x = from_float(obj.get("defaultPivotX"))
        default_pivot_y = from_float(obj.get("defaultPivotY"))
        defs = Definitions.from_dict(obj.get("defs"))
        export_tiled = from_bool(obj.get("exportTiled"))
        external_levels = from_bool(obj.get("externalLevels"))
        flags = from_list(Flag, obj.get("flags"))
        identifier_style = IdentifierStyle(obj.get("identifierStyle"))
        image_export_mode = ImageExportMode(obj.get("imageExportMode"))
        json_version = from_str(obj.get("jsonVersion"))
        level_name_pattern = from_str(obj.get("levelNamePattern"))
        levels = from_list(Level.from_dict, obj.get("levels"))
        minify_json = from_bool(obj.get("minifyJson"))
        next_uid = from_int(obj.get("nextUid"))
        worlds = from_list(World.from_dict, obj.get("worlds"))
        default_level_height = from_union(
            [from_none, from_int], obj.get("defaultLevelHeight")
        )
        default_level_width = from_union(
            [from_none, from_int], obj.get("defaultLevelWidth")
        )
        export_png = from_union([from_none, from_bool], obj.get("exportPng"))
        png_file_pattern = from_union([from_none, from_str], obj.get("pngFilePattern"))
        tutorial_desc = from_union([from_none, from_str], obj.get("tutorialDesc"))
        world_grid_height = from_union(
            [from_none, from_int], obj.get("worldGridHeight")
        )
        world_grid_width = from_union([from_none, from_int], obj.get("worldGridWidth"))
        world_layout = from_union([from_none, WorldLayout], obj.get("worldLayout"))
        return LdtkJSON(
            app_build_id,
            backup_limit,
            backup_on_save,
            bg_color,
            default_grid_size,
            default_level_bg_color,
            default_pivot_x,
            default_pivot_y,
            defs,
            export_tiled,
            external_levels,
            flags,
            identifier_style,
            image_export_mode,
            json_version,
            level_name_pattern,
            levels,
            minify_json,
            next_uid,
            worlds,
            default_level_height,
            default_level_width,
            export_png,
            png_file_pattern,
            tutorial_desc,
            world_grid_height,
            world_grid_width,
            world_layout,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["appBuildId"] = to_float(self.app_build_id)
        result["backupLimit"] = from_int(self.backup_limit)
        result["backupOnSave"] = from_bool(self.backup_on_save)
        result["bgColor"] = from_str(self.bg_color)
        result["defaultGridSize"] = from_int(self.default_grid_size)
        result["defaultLevelBgColor"] = from_str(self.default_level_bg_color)
        result["defaultPivotX"] = to_float(self.default_pivot_x)
        result["defaultPivotY"] = to_float(self.default_pivot_y)
        result["defs"] = to_class(Definitions, self.defs)
        result["exportTiled"] = from_bool(self.export_tiled)
        result["externalLevels"] = from_bool(self.external_levels)
        result["flags"] = from_list(lambda x: to_enum(Flag, x), self.flags)
        result["identifierStyle"] = to_enum(IdentifierStyle, self.identifier_style)
        result["imageExportMode"] = to_enum(ImageExportMode, self.image_export_mode)
        result["jsonVersion"] = from_str(self.json_version)
        result["levelNamePattern"] = from_str(self.level_name_pattern)
        result["levels"] = from_list(lambda x: to_class(Level, x), self.levels)
        result["minifyJson"] = from_bool(self.minify_json)
        result["nextUid"] = from_int(self.next_uid)
        result["worlds"] = from_list(lambda x: to_class(World, x), self.worlds)
        result["defaultLevelHeight"] = from_union(
            [from_none, from_int], self.default_level_height
        )
        result["defaultLevelWidth"] = from_union(
            [from_none, from_int], self.default_level_width
        )
        result["exportPng"] = from_union([from_none, from_bool], self.export_png)
        result["pngFilePattern"] = from_union(
            [from_none, from_str], self.png_file_pattern
        )
        result["tutorialDesc"] = from_union([from_none, from_str], self.tutorial_desc)
        result["worldGridHeight"] = from_union(
            [from_none, from_int], self.world_grid_height
        )
        result["worldGridWidth"] = from_union(
            [from_none, from_int], self.world_grid_width
        )
        result["worldLayout"] = from_union(
            [from_none, lambda x: to_enum(WorldLayout, x)], self.world_layout
        )
        return result


def ldtk_json_from_dict(s: Any) -> LdtkJSON:
    return LdtkJSON.from_dict(s)


def ldtk_json_to_dict(x: LdtkJSON) -> Any:
    return to_class(LdtkJSON, x)
