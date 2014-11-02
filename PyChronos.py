#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Previsão Atendimentos chamados

autor: Cauê Beloni
revisor: Rodolfo Mielitz
Criado: 24/06/2014
"""

import sqlite3
from datetime import *
from time import strptime
from PySide import QtCore, QtGui, QtSql

class DadosSqlModel(QtSql.QSqlQueryModel):
    def flags(self, index):
        flags = super(DadosSqlModel, self).flags(index)

        if index.column() in (1, 2, 3, 7, 8):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (1, 2, 3, 7, 8):
            return False
        primaryKeyIndex = self.index(index.row(), 0)
        self.chamado_corrente = self.data(primaryKeyIndex)

        self.clear()

        if index.column() == 1: #EMPRESA
            ok = self.setEmpresa(self.chamado_corrente, value)
        elif index.column() == 2: #TEMPO DESENVOLVIMENTO
            ok = self.setTempoDesenvolvimento(self.chamado_corrente, value)
        elif index.column() == 3: #DATA INICIAL
            ok = self.setDataInicial(self.chamado_corrente, value)
        elif index.column() == 7: #STATUS
            ok = self.setStatus(self.chamado_corrente, value)
        elif index.column() == 8: #RECURSO
            ok = self.setRecurso(self.chamado_corrente, value)

        self.refresh()
        return ok

    def refresh(self):
        #self.setAtualizaData()

        self.setQuery('select chamado,empresa,tempo_desenvolvimento,data_inicial,data_final,ordem,tipo,status,recurso from ordem_atendimento order by ordem')
        self.setHeaderData(0, QtCore.Qt.Horizontal, "CHAMADO")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "EMPRESA")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "TEMPO DEV.")
        self.setHeaderData(3, QtCore.Qt.Horizontal, "DATA INI.")
        self.setHeaderData(4, QtCore.Qt.Horizontal, "DATA FINAL")
        self.setHeaderData(5, QtCore.Qt.Horizontal, "ORDEM")
        self.setHeaderData(6, QtCore.Qt.Horizontal, "TIPO")
        self.setHeaderData(7, QtCore.Qt.Horizontal, "STATUS")
        self.setHeaderData(8, QtCore.Qt.Horizontal, "RECURSO")

        #frm.table_view.resizeColumnsToContents()
        #defineTamanhoTela();

    def setEmpresa(self, chamado, empresa):
        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set empresa = ? where chamado = ?')
        query.addBindValue(empresa)
        query.addBindValue(chamado)
        self.refresh()
        return query.exec_()

    def setStatus(self, chamado, status):
        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set status = ? where chamado = ?')
        query.addBindValue(status)
        query.addBindValue(chamado)
        self.refresh()
        return query.exec_()

    def setDataInicial(self, chamado, data_inicial):
        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set data_inicial = ? where chamado = ?')
        query.addBindValue(data_inicial)
        query.addBindValue(chamado)
        self.refresh()
        return query.exec_()

    def setRecurso(self, chamado, recurso):
        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set recurso = ? where chamado = ?')
        query.addBindValue(recurso)
        query.addBindValue(chamado)
        self.refresh()
        return query.exec_()

    def setTempoDesenvolvimento(self, chamado, tempoDesenvolvimento):
        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set tempo_desenvolvimento = ? where chamado = ?')
        query.addBindValue(tempoDesenvolvimento)
        query.addBindValue(chamado)

        self.refresh()
        return query.exec_()

    def getCursorCount(self):
        cursor_count = QtSql.QSqlQuery("select count(*) from ordem_atendimento")
        cursor_count.next()
        valor_cursor_count = str(cursor_count.value(0))

        if valor_cursor_count == 'None':
            valor_cursor_count = '0'
        return valor_cursor_count

    def setAlteraOrdem (self, peso):
        valor_cursor_count = self.getCursorCount()

        for index in frm.table_view.selectionModel().selectedRows():
            indexRow = index.row()
            indexOrdem = self.index(index.row(), 5)
            indexChamado = self.index(index.row(), 0)

            dataOrdem = self.data(indexOrdem)
            dataChamado = self.data(indexChamado)

        if dataOrdem == 1 and peso == -1:
            print ("Não é possível priorizar o primeiro atendimento")
            return
        elif str(dataOrdem) == valor_cursor_count and peso == 1:
            print ("Não é possível postergar o último atendimento")
            return

        query = QtSql.QSqlQuery()
        query.prepare('update ordem_atendimento set ordem = ? where ordem = ?')
        query.addBindValue(dataOrdem)
        query.addBindValue(dataOrdem + peso)
        query.exec_()

        query.prepare('update ordem_atendimento set ordem = ? where chamado = ?')
        query.addBindValue(dataOrdem + peso)
        query.addBindValue(dataChamado)
        query.exec_()

        self.refresh()

        frm.table_view.selectRow(indexRow + peso)

    def setPriorizar (self):
        self.setAlteraOrdem(-1)

    def setPostergar (self):
        self.setAlteraOrdem(1)

    def setDataPrevisao (self,tempo_de_desenvolvimento,data):
        #data = '28-10-2014 08:30'
        if len(data) > 16: 
            data = data[4:]
        dia_semana_extenso = {6: 'Dom ', 0: 'Seg ', 1: 'Ter ', 2:'Qua ', 3: 'Qui ', 4:'Sex ', 5: 'Sáb '}
        data_incial = datetime.strptime(data, '%d-%m-%Y %H:%M')
        data_formatada = datetime.strptime(data, '%d-%m-%Y %H:%M')

        hora_diferenca = data_formatada.hour - 8

        if hora_diferenca != 0:
            hora_diferenca *= -1
            data_formatada = data_formatada + timedelta(hours = hora_diferenca)

        tempo = int(tempo_de_desenvolvimento)

        horas = tempo % 8
        #print ("horas: " + str(horas))

        dias = tempo / 8
        #print ("dias: " + str(dias))

        data_days = data_formatada + timedelta(days = dias)
        data_final = data_days + timedelta(hours = horas)

        #adiciona novamente as horas subtraidas para o cálculo de dias e horas
        if hora_diferenca != 0:
            hora_diferenca *= -1
            data_final = data_final + timedelta(hours = hora_diferenca)

        #verifica se o horário de almoço será adicionado somente para o dia corrente
        if ((data_final.hour >= 12 and data_final.hour <= 13) or (data_incial.day != data_final.day and data_final.hour >= 12)):
            data_final = data_final + timedelta(hours = 1)

        #Caso após adicionar a diferença de horas o valor ultrapassar o horário comercial é adicionado mais um dia e inclída as horas da
        #diferença
        if  data_final.hour >= 18:
            hora_diferenca = data_final.hour - 17
            data_final = data_final + timedelta(days = 1)
            dias += 1
            data_final = data_final + timedelta(hours = - data_final.hour)
            data_final = data_final + timedelta(hours = 8 + hora_diferenca)

        # para cada dia de desenvolvimento verifica se existe sábado (dia_semana = 5)
        for i in range(0,dias):
            data_formatada = data_formatada + timedelta(days = 1)
            dia_semana = data_formatada.weekday()
            # se dia da semana for sábado adiciona dois dias a data final
            if (dia_semana == 5):
                data_final = data_final + timedelta(days = 2)
                data_formatada = data_formatada + timedelta(days = 2)

        dia_semana = data_final.weekday()        
        data_final_texto = dia_semana_extenso[dia_semana] + data_final.strftime('%d-%m-%Y %H:%M')
        #print (data_final.strftime('%d-%m-%Y %H:%M'))
        return data_final_texto

    def setAtualizaData (self):
        vPrimerio = True
        q = QtSql.QSqlQuery("select * from ordem_atendimento order by ordem asc")
        rec = q.record()
        colChamado = rec.indexOf("chamado")
        colDataPrevista = rec.indexOf("data_inicial")
        colTempoDesenvolvimento = rec.indexOf("tempo_desenvolvimento")
        query_date = QtSql.QSqlQuery()

        while q.next():
            if vPrimerio:
                vPrimerio = False
                data_final = self.setDataPrevisao(q.value(colTempoDesenvolvimento),q.value(colDataPrevista))
                query_date.prepare('update ordem_atendimento set data_final = ? where chamado = ?')
                query_date.addBindValue(data_final)
                query_date.addBindValue(q.value(colChamado))
                query_date.exec_()
            else:
                query_date.prepare('update ordem_atendimento set data_inicial = ? where chamado = ?')
                query_date.addBindValue(data_final)
                query_date.addBindValue(q.value(colChamado))

                query_date.exec_()

                data_final = self.setDataPrevisao(q.value(colTempoDesenvolvimento),data_final)

                query_date.prepare('update ordem_atendimento set data_final = ? where chamado = ?')
                query_date.addBindValue(data_final)
                query_date.addBindValue(q.value(colChamado))

                query_date.exec_()

        self.refresh()

    def setInserirChamado(self,numero_chamado,empresa,tempo_desenvolvimento,tipo_chamado):
        valor_cursor_count = int(self.getCursorCount()) + 1
        data_atual = datetime.now()
        data_atual = data_atual.strftime('%d-%m-%Y %H:%M')
        query = QtSql.QSqlQuery()
        query.prepare('insert into ordem_atendimento(chamado,empresa,tempo_desenvolvimento,tipo,ordem,data_inicial) values (?,?,?,?,?,?)')
        query.addBindValue(numero_chamado)
        query.addBindValue(empresa)
        query.addBindValue(tempo_desenvolvimento)
        query.addBindValue(tipo_chamado)
        query.addBindValue(valor_cursor_count)
        query.addBindValue(data_atual)
        query.exec_()
        #print (type(data_atual))

        return True

    def setDeletarChamado(self):
        valor_cursor_count = int(self.getCursorCount()) + 1

        for index in frm.table_view.selectionModel().selectedRows():
            indexChamado = self.index(index.row(), 0)
            indexOrdem = self.index(index.row(), 5)

            dataOrdem = self.data(indexOrdem)
            dataChamado = self.data(indexChamado)

        query = QtSql.QSqlQuery()
        query.prepare('delete from ordem_atendimento where chamado = ?')
        query.addBindValue(dataChamado)
        query.exec_()

        for i in range(dataOrdem,valor_cursor_count):
                query.prepare('update ordem_atendimento set ordem = ? where ordem = ?')
                query.addBindValue(dataOrdem)
                query.addBindValue(dataOrdem+1)

                dataOrdem += 1

                query.exec_()

        self.refresh()
        return True

class FrmMenu(QtGui.QWidget):
    def __init__(self,title, model):
        super(FrmMenu, self).__init__()

        self.setWindowTitle("Previsao Atendimentos - DBA")

        hbox = QtGui.QGridLayout()

        self.table_view = QtGui.QTableView()
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(5,True)
        self.table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_view.resizeColumnsToContents()
        self.table_view.selectRow(0)
        #print (self.table_view.columnWidth(1))
        # handle ao alterar seleção de row em table_view
        #self.table_selecao = self.table_view.selectionModel()
        #self.table_selecao.selectionChanged.connect(editableModel.setPriorizar)

        x, y, w, h = 300, 300, 134, 300
        for i in range(0,9):
            w += self.table_view.columnWidth(i)
        self.setGeometry(x, y, w, h)

        self.btnPriorizar = QtGui.QPushButton('&Priorizar', self)
        self.btnPostergar = QtGui.QPushButton('P&ostergar', self)
        self.btnInserir   = QtGui.QPushButton('&Inserir', self)
        self.btnExcluir   = QtGui.QPushButton('&Excluir', self)
        self.btnRefresh   = QtGui.QPushButton('&Refresh', self)

        hbox.addWidget(self.table_view, 0, 2, 6, 1)
        hbox.addWidget(self.btnPriorizar,0,1)
        hbox.addWidget(self.btnPostergar,1,1)
        hbox.addWidget(self.btnInserir,2,1)
        hbox.addWidget(self.btnExcluir,3,1)
        hbox.addWidget(self.btnRefresh,4,1)

        self.setLayout(hbox)

    def show_and_raise(self):
        self.show()
        self.raise_()

class FrmInserir(QtGui.QDialog):

    def __init__(self):
        super(FrmInserir, self).__init__()

        self.createFormGroupBox()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        #editableModel.setInserirChamado('6000','Red Hat','8','R')
        buttonBox.accepted.connect(self.inserirChamado)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Inserir novo chamado")

    def createFormGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("")
        layout = QtGui.QFormLayout()
        self.lineEditChamado          = QtGui.QLineEdit()
        self.lineEditEmpresa          = QtGui.QLineEdit()
        self.spinTempoDesenvolvimento = QtGui.QSpinBox()
        self.lineEditTipo             = QtGui.QLineEdit()

        layout.addRow(QtGui.QLabel("Numero chamado:"), self.lineEditChamado)
        layout.addRow(QtGui.QLabel("Empresa:"), self.lineEditEmpresa)
        layout.addRow(QtGui.QLabel("Tempo desenvolvimento:"), self.spinTempoDesenvolvimento)
        layout.addRow(QtGui.QLabel("Tipo do chamado:"), self.lineEditTipo)
        self.formGroupBox.setLayout(layout)

    def inserirChamado(self):
        if dados_sql_model.setInserirChamado(frmInserir.lineEditChamado.text(),frmInserir.lineEditEmpresa.text(),frmInserir.spinTempoDesenvolvimento.text(),frmInserir.lineEditTipo.text()):
            print ("Inserido com sucesso")
        else:
            print ("Erro ao inserir registro")
        #editableModel.refresh()
        frmInserir.close()

def defineTamanhoTela():
        x, y, w, h = 0, 0, 223, 0
        for i in range(0,8):
            w += frm.table_view.columnWidth(i)
        print (w)
        frm.setGeometry(x, y, w, h)

def abreConexao():
    ''' Abreconexao (nome do banco de dados sqlite)
    '''
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('dados.db')
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                QtGui.qApp.tr("Não é possível acessar Banco de dados.\n"
                              "This example needs SQLite support. Please read "
                              "the Qt SQL driver documentation for information "
                              "how to build it.\n\nClick Cancel to exit."),
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
        return False

    query = QtSql.QSqlQuery()
    return True

def printaMensagem():
    print ("Printado")
    print (frmInserir.lineEditChamado.text())

def initializeModel(model):
    model.setQuery('select chamado,empresa,tempo_desenvolvimento,data_inicial,data_final,ordem,tipo,status,recurso from ordem_atendimento order by ordem')
    model.setHeaderData(0, QtCore.Qt.Horizontal, "CHAMADO")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "EMPRESA")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "TEMPO DEV.")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "DATA INI.")
    model.setHeaderData(4, QtCore.Qt.Horizontal, "DATA FINAL")
    model.setHeaderData(5, QtCore.Qt.Horizontal, "ORDEM")
    model.setHeaderData(6, QtCore.Qt.Horizontal, "TIPO")
    model.setHeaderData(7, QtCore.Qt.Horizontal, "STATUS")
    model.setHeaderData(8, QtCore.Qt.Horizontal, "RECURSO")

def abrirFormInserir():
    frmInserir.exec_()
    #sys.exit(frmInserir.exec_())

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('organize.ico'))

    if not abreConexao():
        sys.exit(1)

    dados_sql_model = DadosSqlModel()
    frmInserir = FrmInserir()

    initializeModel(dados_sql_model)
    frm = FrmMenu("Editable Query Model", dados_sql_model)
    frm.btnPriorizar.clicked.connect(dados_sql_model.setPriorizar)
    frm.btnPostergar.clicked.connect(dados_sql_model.setPostergar)
    frm.btnRefresh.clicked.connect(dados_sql_model.setAtualizaData)
    frm.btnInserir.clicked.connect(abrirFormInserir)
    frm.btnExcluir.clicked.connect(dados_sql_model.setDeletarChamado)
    frm.show()

    sys.exit(app.exec_())