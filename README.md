# MultiMagNet (Disciplina GA-031)

_Código-fonte e implementação dos casos de testes relatados no Trabalho 2._

## Instalando as dependências

```
$ sudo pip3 install python-mnist
```
```
$ sudo pip3 install numpy
```
```
$ sudo pip3 install sklearn
```
## Executando o _MultiMagNet_

1. Adicione a pasta _modules_ no `PYTHONPATH`:

```
$ export PYTHONPATH="$PYTHONPATH:/path_to_project_folder/modules"
```

2. Na pasta do projeto (`MultiMagNet_GA031`), execute o seguinte comando no terminal para iniciar o _MultiMagNet_:

```
$ python3 modules/__main__.py
```

# Running the tests

1. Adicione a pasta _tests_ no no `PYTHONPATH`:

```
$ export PYTHONPATH="$PYTHONPATH:/path_to_project_folder/tests"
```

2. Na pasta do projeto (`MultiMagNet_GA031`), execute o seguinte comando no terminal para iniciar os testes do _MultiMagNet_:

```
$ python3 tests/__main__.py
```