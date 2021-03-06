import typing
import os
import numbers
import random
import csv


class SLoc:
    def __init__(self, s: typing.Dict[str, typing.Any]):
        self.series = s

    def __getitem__(self, key):
        if issubclass(type(key), numbers.Number):
            return self.series[str(key)]
            # return list(self.series.values())[key]
        # if type(key) == slice:
        #     return list(self.series.values())[key]
        # if type(key) == typing.List[bool]:
        #     return [list(self.series.values())[i] for i, x in enumerate(key) if x]
        # if type(key) == tuple:
        #     ans = DataFrame()
        #     for i, s in self.series.items():
        #         if s[key[0]] == key[1]:
        #             ans.add(i, s)
        #     return ans
        if type(key) == str:
            return self.series[key]
        print("KEY:", key, type(key))
        raise KeyError("Unexpected key type")

    def __setitem__(self, key, value):
        if type(key) == int:
            k, v = list(self.series.values())[key]
            self.series[k] = v
        if type(key) == slice:
            for k, _ in list(self.series.values())[key]:
                self.series[k] = value
        if type(key) == typing.List[bool]:
            for k, _ in [list(self.series.values())[i] for i, x in enumerate(key) if x]:
                self.series[k] = value
        raise KeyError("Unexpected key type")


class SILoc:
    def __init__(self, s: typing.Dict[str, typing.Any]):
        self.series = s

    def __getitem__(self, key):
        if issubclass(type(key), numbers.Number):
            return list(self.series.values())[key]
        # if type(key) == slice:
        #     return list(self.series.values())[key]
        # if type(key) == typing.List[bool]:
        #     return [list(self.series.values())[i] for i, x in enumerate(key) if x]
        if type(key) == tuple:
            ans = DataFrame()
            for i, s in self.series.items():
                if s[key[0]] == key[1]:
                    ans.add(i, s)
            return ans
        if type(key) == str:
            return self.series[key]
        print("KEY:", key, type(key))
        raise KeyError("Unexpected key type")

    def __setitem__(self, key, value):
        if type(key) == int:
            k, v = list(self.series.values())[key]
            self.series[k] = v
        if type(key) == slice:
            for k, _ in list(self.series.values())[key]:
                self.series[k] = value
        if type(key) == typing.List[bool]:
            for k, _ in [list(self.series.values())[i] for i, x in enumerate(key) if x]:
                self.series[k] = value
        raise KeyError("Unexpected key type")


class Series:
    def __init__(self):
        self.data: typing.Dict[str, typing.Any] = {}

    def __eq__(self, obj):
        if isinstance(obj, Series):
            return self.data == obj.data
        result = Series()
        for k, v in self.data.items():
            # print(str(k), str(obj))
            result.add(k, str(v) == str(obj))
        return result

    def __str__(self):
        return " ".join([f"{k}: {v}" for k, v in self.data.items()])

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        try:
            # print(self.data[item], "-", self.data)
            return self.data[item]
        except KeyError as e:
            print(f"could not find key '{item}'")
            print(self.data.keys())
            raise e

    def __setitem__(self, key, value):
        self.data[key] = value

    def add(self, index: str, d):
        self.data[index] = d

    def apply(self, f: typing.Callable[[str], str]):
        for i, d in self.data.items():
            self.data[i] = f(d)
        return self

    def map(self, f):
        for i, d in self.data.items():
            self.data[i] = f(d)
        return self

    def items(self):
        return self.data.items()

    def copy(self):
        result = Series()

        for k, v in self.items():
            result.add(k, v)
        return result

    def lower(self):
        result = Series()

        for k, v in self.items():
            result.add(k, str(v).lower())
        return result

    @property
    def loc(self):
        return SLoc(self.data)

    @property
    def iloc(self):
        return SILoc(self.data)


class DFLoc:
    def __init__(self, df: typing.Dict[str, Series]):
        self.dataframe = df

    def __getitem__(self, key):
        if issubclass(type(key), numbers.Number):
            return self.dataframe[str(key)]
            # return list(self.dataframe.values())[key]
        # if type(key) == slice:
        #     return self.dataframe[key]
        #     # return list(self.dataframe.values())[key]
        # if type(key) == typing.List[bool]:
        #     return self.dataframe[key]
        #     # return [list(self.dataframe.values())[i] for i, x in enumerate(key) if x]
        if type(key) == tuple:
            return self.dataframe[str(key[0])][str(key[1])]
            # ans = DataFrame()
            # for i, s in self.dataframe.items():
            # if s[key[0]] == key[1]:
            #     ans.add(i, s)
            # return ans
        if type(key) == str:
            return self.dataframe[str(key)]
        raise KeyError("Unexpected key type")

    def __setitem__(self, key, value):
        if type(key) == int:
            for s in list(self.dataframe.values())[key]:
                for k, _ in s.items():
                    s[k] = value
        if type(key) == slice:
            for series in list(self.dataframe.values())[key]:
                for s in series:
                    for k, _ in s.items():
                        s[k] = value
        if type(key) == typing.List[bool]:
            for s in [list(self.dataframe.values())[i] for i, x in enumerate(key) if x]:
                for k, _ in s.items():
                    s[k] = value
        raise KeyError("Unexpected key type")


class DFILoc:
    def __init__(self, df: typing.Dict[str, Series]):
        self.dataframe = df

    def __getitem__(self, key):
        if issubclass(type(key), numbers.Number):
            return list(self.dataframe.values())[key]
        if type(key) == slice:
            result = DataFrame()

            for k, v in list(self.dataframe.items())[key]:
                result.add(k, v.copy())
            return result
        #     # return list(self.dataframe.values())[key]
        # if type(key) == typing.List[bool]:
        #     return self.dataframe[key]
        #     # return [list(self.dataframe.values())[i] for i, x in enumerate(key) if x]
        # if type(key) == tuple:
        # return self.dataframe[key[0]]
        # ans = DataFrame()
        # for i, s in self.dataframe.items():
        # if s[key[0]] == key[1]:
        #     ans.add(i, s)
        # return ans
        # if type(key) == str:
        #     return self.dataframe[key]
        raise KeyError("Unexpected key type")

    def __setitem__(self, key, value):
        if type(key) == int:
            for s in list(self.dataframe.values())[key]:
                for k, _ in s.items():
                    s[k] = value
        if type(key) == slice:
            for series in list(self.dataframe.values())[key]:
                for s in series:
                    for k, _ in s.items():
                        s[k] = value
        if type(key) == typing.List[bool]:
            for s in [list(self.dataframe.values())[i] for i, x in enumerate(key) if x]:
                for k, _ in s.items():
                    s[k] = value
        raise KeyError("Unexpected key type")


class DFAttrMethods:
    def __init__(self, df, attr_name: str):
        self.df = df
        self.attr_name = attr_name

    def __eq__(self, other):
        ans = DataFrame()
        for i, s in self.df.items():
            if s[self.attr_name] == other:
                ans.add(i, s)
        return ans


class DataFrame:
    def __init__(self):
        self.data: typing.Dict[str, Series] = {}

    def __str__(self):
        return "\n".join([f"{k}: {v}" for k, v in self.data.items()])

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return str(item) in self.data

    def __getattr__(self, item):
        return DFAttrMethods(self.data, item)

    def __getitem__(self, item):
        if isinstance(item, Series):
            result = DataFrame()
            for k, v in item.items():
                if (k in self.data) and v:
                    result[k] = self.loc[k]
            return result
        item = str(item)
        ans = Series()
        for k, v in self.data.items():
            ans.add(k, v[item])
        return ans

    def __setitem__(self, key, value):
        self.data[str(key)] = value

    def add(self, index: str, s: Series):
        self.data[str(index)] = s

    def apply(self, f: typing.Callable[[str], str]) -> "DataFrame":
        for i, s in self.data.items():
            for k, v in s.items():
                if hasattr(s[k], str(f)):
                    s[k] = f(v)
        return self

    def map(self, f) -> "DataFrame":
        for i, s in self.data.items():
            for k, v in s.items():
                s[k] = f(v)
        return self

    def map_attr(self, attr, f) -> "DataFrame":
        for i, s in self.data.items():
            s[attr] = f(s[attr])
        return self

    def sample(self):
        return random.choice(list(self.data.values()))

    @property
    def loc(self):
        return DFLoc(self.data)

    @property
    def iloc(self):
        return DFILoc(self.data)


def read_csv(
    path: typing.Union[str, bytes, os.PathLike],
    header: typing.Optional[bool] = True,
    names: typing.List[str] = None,
    index_col: int = None,
    comment: str = None,
    verbose=False,
) -> DataFrame:

    try:
        with open(path, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            first_row = next(reader)
            if names is not None:
                col_names = names
            elif header:
                col_names = first_row
            else:
                col_names = list(range(len(first_row)))
            df = DataFrame()
            for line in reader:
                if comment is not None:
                    if line[0][0 : len(comment)] == comment:
                        continue

                s = Series()

                if index_col is not None:
                    index = line[index_col]
                else:
                    index = len(df)

                for j, value in enumerate(line):
                    s.add(col_names[j] if j != index_col else "id", value)
                df.add(index, s)
        if verbose:
            print(df)
        return df
    except OSError as e:
        print(f"Could not find csv file at {path}")
        raise e

