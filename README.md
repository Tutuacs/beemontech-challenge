<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://www.svgrepo.com/show/353657/django-icon.svg" alt="Project logo"></a>
</p>

<h3 align="center">Beemôn challenge</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Tutuacs/beemontech-challenge/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Tutuacs/beemontech-challenge/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Este projeto foi feito para comprovar experiência e conhecimentos para a vaga com foco em webscraping com python, Django. O desafio escolhido foi com o site <a href= "https://quotes.toscrape.com/">quotes</a>.
    <br> 
</p>

## 📝 Conteúdos

- [Sobre](#about)
- [Iniciando](#getting_started)
- [Deploy](#deployment)
- [Uso](#usage)
- [Feito com](#built_using)
- [Desenvolvido por](#authors)
- [Finalização](#acknowledgement)

## 🧐 Sobre <a name = "about"></a>

Este projeto é um desafio de webscrapping, onde o objetivo é extrair informações de uma página web e armazená-las em um banco de dados. O projeto utiliza Django como framework web e Sqlite ou PostgreSQL como banco de dados.

## 🏁 Iniciando <a name = "getting_started"></a>

Estas instruções permitirão que você obtenha uma cópia do projeto em execução na sua máquina local para fins de desenvolvimento e teste. Veja a seção de [deploy](#deployment) para saber como rodar o projeto.

### Pré-requisitos

Para rodar o projeto corretamente, você precisará ter instalado em sua máquina:

```
Docker
```

### Instalação

Passo a passo, realize os seguintes passos para rodar o projeto:

Install docker

```
https://docs.docker.com/engine/install/
```

Clone the repository

```sh
git clone https://github.com/Tutuacs/beemontech-challenge.git
```

Using VsCode?

```sh
code beemontech-challenge
```

## 🚀 Deploy <a name = "deployment"></a>

Para fazer o deploy do projeto, você pode usar o Docker para criar um container com Redis, PostgreSQL, API e Service.

```sh
sudo docker compose up -d --build
```

Acessar a aplicação no navegador:

```
http://localhost:8000/swagger
```

A api principal funciona sem Redis, mas não terá a funcionalidade de agendamento de updates. Para que funcione corretamente, é necessário rodar o serviço subscribe, que irá escutar as mensagens do Redis e executar as tarefas de scraping no período programado, nesta branch o docker está configurado para rodar automaticamente ambos, servidor e serviço.

## 📌 Uso <a name = "usage"></a>

Principais rotas:
- [/live](http://localhost:8000/swagger) - Mostra os dados atuais do site
- [/update](http://localhost:8000/swagger) - Atualiza os dados do banco de dados com os dados mais recentes do site, apenas criando novos dados não existentes.
- [/pandas/csv](http://localhost:8000/swagger) - Gera um DataFrame CSV com os dados atuais do banco de dados, utilizando a biblioteca Pandas.
- [/pandas/json](http://localhost:8000/swagger) - Gera um DataFrame JSON com os dados atuais do banco de dados, utilizando a biblioteca Pandas.
- [{POST} /schedule](http://localhost:8000/swagger) - Agenda uma tarefa de scraping para ser executada em um período específico, utilizando o Redis como broker de mensagens.

## ⛏️ Feito com <a name = "built_using"></a>

- [PostgreSQL](https://www.postgresql.org/) - Database
- [Django](https://www.djangoproject.com/) - Server Framework
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - Scraping Library
- [Redis](https://redis.io/) - Message Broker
- [Docker](https://www.docker.com/) - Containerization Platform

## ✍️ Desenvolvido por <a name = "authors"></a>

- [@ArthurSilva](https://github.com/Tutuacs) - Dev

See also the list of [contributors](https://github.com/Tutuacs/beemontech-challenge/contributors) who participated in this project.

## 🎉 Finalização <a name = "acknowledgement"></a>

- IMPORTATE: Ao criar uma *"schedule"*, a data enviada não é verificada, criando com uma data menor que a data atual resultará uma schedule com status FAIL.

##### Melhorias Importantes:
  - Rota */live* deveria ser feita com Ws para que o usuário possa acompanhar as atualizações em tempo real, para isso, seria necessário alterar a função que faz o scraping para receber uma conexão WebSocket e enviar os dados atualizados para a conexão recebida conforme o scraping é feito.
  - Rota */update* deveria ser feita usando Redis Pub/Sub, publicando os objetos encontrados no scraping para que outro serviço possa cuidar da parte de salvar os dados no banco de dados, assim, o serviço de scraping não ficaria bloqueado e a resposta da rota */update* seria mais rápida.

##### References

  - [Django Video](https://youtu.be/XAzVlnPDVd0?si=HPWwvPxa0ugR4AMz)
  - [Python && Redis](https://dev.to/felipepaz/python-e-redis-utilizando-pubsub-51fo)
  - [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - [Pandas](https://www.w3schools.com/Python/pandas/pandas_dataframes.asp)
