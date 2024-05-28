# Moorgen Home Assistant component
## Установка компонента
Скопировать файлы репозитория в папку `<config>/custom-components/moorgen_smart_panel`, где \<config\> - папка конфигурации Home Assistan
Скомпилировать двоичный файл общего объекта:
```
cd remoorgen-go/
go build -o remoorgen.so -buildmode=c-shared github.com/Dora-Development/remoorgen-go/cmd
```
Добавить в файл `<config>/configuration.yaml` код:
```
remoorgen_smart_panel:
```
