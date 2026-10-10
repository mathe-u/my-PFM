# Documento de Requisitos: Aplicação Web de Gestão Financeira Compartilhada (PFM)

## 1. Visão Geral do Sistema

O sistema é uma aplicação web (Personal Finance Management - PFM) projetada para facilitar o acompanhamento e a gestão de finanças colaborativas. O objetivo principal é permitir que múltiplos usuários em um mesmo "grupo financeiro" registrem receitas, dividam despesas, definam orçamentos e acompanhem metas financeiras de forma transparente e sincronizada.

## 2. Atores (Perfis de Usuário)

* **Proprietário do Grupo (Admin):** Usuário que cria o grupo financeiro. Tem permissão para convidar novos membros, remover membros e alterar configurações globais do grupo.
* **Membro do Grupo:** Usuário convidado. Pode registrar transações, visualizar dashboards, criar categorias e editar seus próprios lançamentos.
* **Usuário Individual:** Usuário que utiliza o sistema apenas para gestão financeira pessoal, sem compartilhar dados (estado padrão antes de criar ou entrar em um grupo).

## 3. Requisitos Funcionais (RF)

### 3.1. Gestão de Usuários e Grupos

* **RF01 - Autenticação:** O sistema deve permitir o cadastro e login de usuários via e-mail/senha.
* **RF02 - Gestão de Perfil:** O usuário deve poder editar seus dados pessoais e preferências (moeda, idioma, fuso horário).
* **RF03 - Criação de Grupos:** O usuário deve poder criar um "Grupo Financeiro" (ex: Casa, Viagem, Casal).
* **RF04 - Convites para o Grupo:** O Administrador deve poder gerar um link de convite.

### 3.2. Gestão de Transações

* **RF05 - Lançamento de Receitas/Despesas:** O sistema deve permitir o registro de transações com os seguintes dados: valor, data, descrição, categoria e conta de origem/destino. Os lançamentos pessoais não devem ser considerados despesas ou receitas compartilhadas automaticamente.

* **RF06 - Divisão de Despesas (Split):** No registro de uma despesa, o sistema deve permitir a divisão do valor entre os membros do grupo de três formas:
* Igualitária (ex: 50/50).
* Porcentagem personalizada (ex: 70/30).
* Valor fixo exato para cada membro.

* **RF07 - Integridade da Divisão:** Ao dividir uma despesa, a soma das partes (em porcentagem ou valor absoluto) deve ser exatamente igual a 100% ou ao valor total da transação.

* **RF08 - Transferências entre contas:** O sistema deve permitir que o usuário registre transferências de valores entre duas contas financeiras, informando a conta de origem, a conta de destino, o valor, a data e uma descrição opcional. A operação deve atualizar os saldos das contas envolvidas de maneira consistente, sem contabilizar a transferência como receita ou despesa.

* **RF09 - Acertos de contas entre membros:** O sistema deve permitir que os membros registrem pagamentos realizados para quitar dívidas decorrentes de despesas compartilhadas, informando o pagador, o beneficiário, o valor, a data e uma descrição opcional. O registro deve atualizar os saldos devidos entre os membros sem contabilizar o pagamento como uma nova receita ou despesa.
* Os acertos devem ser vinculados a uma despesa que foi dividida entre os membros.
* O valor de um acerto não pode ser negativo ou igual a zero.
* O valor de um acerto não pode superar a dívida pendente, salvo se o sistema permitir pagamentos antecipados ou créditos.
* Apenas membros autorizados podem registrar ou editar acertos.
* A operação deve pertencer ao grupo financeiro correto.
* O sistema deve impedir que uma falha parcial deixe os registros financeiros inconsistentes.
* O sistema apenas registra transferência entre contas e acertos entre membros, não executa nada em bancos reais.

* **RF10 - Transações Recorrentes:** O sistema deve permitir a configuração de despesas ou receitas que se repetem (mensal, semanal, anual).

### 3.3. Organização e Planejamento

* **RF11 - Gestão de Categorias:** O sistema deve permitir a criação, edição e exclusão de categorias.
* **RF12 - Definição de Orçamentos (Budgets):** Os usuários devem poder estabelecer limites de gastos mensais por categoria, recebendo alertas visuais quando o limite estiver próximo (ex: 80%) ou for ultrapassado.
* **RF13 - Gestão de Metas (Goals):** O grupo deve poder criar metas de economia (ex: "Viagem de Férias"), definindo um valor alvo, data limite e registrando aportes mensais.

### 3.4. Visualização e Relatórios

* **RF14 - Dashboard Interativo:** O sistema deve apresentar um painel principal com:
* Saldo total consolidado e saldo por conta.
* Gráfico de receitas vs. despesas do mês.
* Resumo de quem deve a quem (acertos pendentes no grupo).


* **RF15 - Extrato Detalhado:** O sistema deve fornecer uma lista filtrável de todas as transações (por data, membro, categoria).

---

## 4. Regras de Negócio (RN)


* **RN01 - Exclusão de Transações:** Uma transação compartilhada só pode ser editada ou excluída pelo autor do lançamento ou pelo Administrador do grupo.
* **RN02 - Fechamento de Fatura/Mês:** Saldos de "quem deve a quem" devem ser calculados dinamicamente com base nas despesas compartilhadas pagas por um único membro em nome do grupo.

---

## 5. Requisitos Não Funcionais (RNF) e Diretrizes de Arquitetura

Para garantir manutenibilidade, escalabilidade e qualidade do software, o sistema deve seguir as diretrizes abaixo:

### 5.1. Arquitetura e Engenharia de Software

* **RNF01 - Padrões Arquiteturais:** O backend deve ser estruturado utilizando **Clean Architecture** em conjunto com princípios de **Domain-Driven Design (DDD)**. A lógica central de finanças (divisão de contas, cálculo de saldos) deve ser completamente isolada de frameworks web ou bancos de dados.
* **RNF02 - Qualidade de Código:** O projeto deve ter testes de unidades para o nucleo de regras de negócio, garantindo ampla cobertura em cálculos financeiros e divisões de despesas.

### 5.2. Stack Tecnológica

* **RNF03 - API RESTful:** A comunicação entre frontend e backend deve ocorrer através de uma API REST bem documentada. O backend pode ser implementado em **TypeScript (Node.js com Fastify)** para alta performance ou **Python (Django REST Framework)** para desenvolvimento ágil.
* **RNF04 - Banco de Dados:** O sistema deve utilizar um banco de dados relacional para garantir a integridade transacional (ACID) das operações financeiras. Um banco como **PostgreSQL** é recomendado para produção, podendo-se adotar **SQLite** para os testes automatizados rápidos e ambientes de desenvolvimento locais.

### 5.3. Usabilidade e Segurança

* **RNF05 - Responsividade:** A interface web deve ser responsiva e otimizada para uso em dispositivos móveis (Mobile First), visto que lançamentos financeiros frequentemente ocorrem "on the go".
* **RNF06 - Segurança de Dados:** As senhas devem ser armazenadas com hash criptográfico (ex: bcrypt/argon2). A autenticação da API deve utilizar tokens JWT com expiração configurada.

* **RNF07 - Operacoes Atomicas:** O sistema deve garantir que as operacoes financeiras sejam atomicas, ou seja, que sejam executadas completamente ou nenhuma parte delas seja executada. Caso ocorra alguma falha durante a execucao de uma operacao, o sistema deve reverter todas as operacoes realizadas ate o momento, garantindo a integridade dos dados.

* **RNF08 - Rotas publicas:** As rotas públicas podem ser acessadas sem autenticação, mas devem ser protegidas por rate limiting.
- /api/auth/login
- /api/auth/register

* **RNF09 - Rotas protegidas:** As rotas protegidas devem ser acessadas apenas com autenticação e devem ter rate limiting.
- /api/groups
- /api/transactions
- /api/budgets
- /api/goals
- /api/categories
- /api/users
