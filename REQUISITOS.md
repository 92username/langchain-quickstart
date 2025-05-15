# ✅ REQUISITOS DO CHATBOT — Projeto EducaMais.tech

## 🎯 Objetivo

Este chatbot tem como objetivo **apoiar o desenvolvimento da startup EducaMais.tech** ao fornecer respostas inteligentes e contextualizadas com base na documentação interna do projeto.

Ele será utilizado para:

- Responder automaticamente aos stakeholders sobre o projeto;
- Utilizar como parâmetro de resposta a **documentação do projeto**, que será adicionada **de forma contínua e dinâmica**;
- Apoiar os próprios **membros da equipe**, promovendo **alinhamento e consistência** nos objetivos e decisões;
- Atuar como ferramenta de **comunicação e validação externa** durante o processo de incubação no **Startup Experience Estácio**.

## 👥 Stakeholders

- Membros do grupo da startup;
- Participantes de outras startups da competição;
- Organizadores do Startup Experience Estácio;
- Banca entrevistadora;
- Comissão avaliadora;
- Comissão julgadora.

---

## ✅ RF — Requisitos Funcionais

- [x] **RF01**: O chatbot deve ser capaz de responder perguntas com base na documentação interna do projeto.
- [x] **RF02**: Deve ser possível inserir novos documentos (.md, .pdf, etc) para atualizar o contexto do chatbot.
- [x] **RF03**: O chatbot deve responder todas as perguntas dos stakeholders e **bloquear perguntas que não estejam relacionadas ao projeto Startup Experience Estácio**, como medida de segurança para proteger nossas chaves de API.
- [x] **RF04**: O sistema deve permitir perguntas referentes ao Startup Experience - Estácio dos usuários via interface web.
- [ ] **RF05**: O chatbot deve solicitar feedback do usuário após cada resposta.
- [x] **RF06**: O chatbot deve exibir uma mensagem informando que as perguntas poderão ser usadas para aprimorar a IA e o projeto.
- [x] **RF07**: Deve oferecer sugestões de perguntas iniciais para orientar novos usuários.
- [ ] **RF08**: A interface deve respeitar a paleta de cores definida pelo time de UX/UI.
- [x] **RF09**: Interface com suporte a modo claro/escuro (light/dark mode).
- [ ] **RF10**: Respostas devem estar formatadas em Markdown, com destaque visual para títulos, listas e links.
- [ ] **RF11**: O chatbot deve conseguir responder tanto em português quanto em inglês, quando solicitado.
- [x] **RF12**: O sistema deve registrar um log de perguntas dos usuários para geração posterior de um FAQ.
- [ ] **RF13**: Criar um log com as tecnologias utilizadas durante a construção do projeto e calcular o quanto foi economizado com o uso do GitHub Student Pack, para demonstrar o impacto prático.

---

## ✅ RNF — Requisitos Não Funcionais

- [ ] **RNF01**: O sistema deve ser hospedado preferencialmente na AWS ou Azure.
- [x] **RNF02**: A VPS da Hostinger pode ser usada como backup do projeto.
- [x] **RNF03**: O domínio próprio utilizado será `educamais.tech`.
- [x] **RNF04**: Deve ser possível realizar deploy via CI/CD (GitHub Actions ou alternativa).
- [ ] **RNF05**: A base de conhecimento deve estar organizada e versionada no GitHub.
- [ ] **RNF06**: O tempo médio de resposta do chatbot **não deve exceder 5 segundos** (⚠️ *ainda não avaliado*).
- [x] **RNF07**: O backend deve ser implementado em Python (Reflex) com integração ao LLM via API.
- [ ] **RNF08**: O sistema deve evitar conflitos de contexto quando múltiplos usuários estiverem utilizando o chatbot simultaneamente. *(Importante verificar se há isolamento de sessão adequado no backend da LLM)*.
- [ ] **RNF09**: Deve haver logs básicos de uso para fins de melhoria contínua (sem violar privacidade).
- [ ] **RNF10**: O projeto deve utilizar preferencialmente tecnologias gratuitas ou com benefício educacional do GitHub Student Pack.

---

## 🔁 Validação e Acompanhamento

Este documento será atualizado continuamente conforme os requisitos forem sendo cumpridos. A marcação dos checkboxes e a documentação das decisões técnicas servirão como fonte de verdade para todos os membros do projeto e como apoio nas apresentações para banca e jurados.

---
