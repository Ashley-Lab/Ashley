import collections


class Cache(collections.OrderedDict):
    """
    Faz a mesma coisa que um OrderedDict, mas com um limite de dados.

    Notas
    -----
    Utilize o método `add` ou a função `setattr` para definir algo. Em
    ambas rotinas se retorna algo, se o cache estiver cheio, o retorno
    será o dado mais antigo colocado em cache e será removido.

    Parâmetros
    ----------
    limit : typing.Optional[int]
        Limite de coisas que podem ser adicionadas. Se nenhum valor for
        informado, não haverá limite.

    Atributos
    ---------
    limit : int
        Limite de coisas que podem ser adicionadas.
    """
    def __init__(self, limit: int = None):
        super().__init__()

        self.limit = limit if limit is not None else -1

    def __setitem__(self, *args):
        item_poped = None
        if len(self) == self.limit:
            item_poped = self.popitem(last=False)

        super().__setitem__(*args)
        return item_poped

    def add(self, name, value):
        """
        Adiciona um item no cache.

        Parâmetros
        ----------
        name : typing.Any
            Nome da coisa que será adicionada.
        value : typing.Any
            Coisa que será adicionada.

        Retornos
        --------
        typing.Any
        """
        return self.__setitem__(name, value)

    def remove(self, key):
        """
        Remove um item no cache.

        Parâmetros
        ----------
        key : typing.Any
            Chave da coisa que será removida.
        """
        del self[key]
