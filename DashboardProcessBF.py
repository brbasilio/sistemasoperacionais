import os  #biblioteca para 
import time #biblioteca para timer e usada para atualização
import threading #biblioteca para threads
import stat
from PyQt6.QtWidgets import QApplication, QHeaderView, QHBoxLayout, QListWidget,QListWidgetItem, QTreeWidget,QTreeWidgetItem, QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem , QFrame, QTabWidget, QMessageBox, QTextEdit, QSizePolicy #biblioteca grafica do PhytonQt6
from PyQt6.QtCore import QTimer, Qt, pyqtSignal #biblioteca grafica do PyQt6

#classe que representa o modelo no MVC

class ProcessInformation:  #Dados para guardar os dados necessarios do processo
    def __init__(self,pid,user,name) :
        self.pid = pid
        self.user = user
        self.name = name

class CPUUsageWidget(QFrame): #classe para fazer a caixa do CPU Usage
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("CPU usage"))

class MemoryUsageWidget(QFrame): #classe para fazer a caixa do Memory Usage
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Memory Usage"))

        self.memory_info_label = QLabel()
        layout.addWidget(self.memory_info_label)

        self.setMaximumHeight(300)
        self.setMinimumWidth(400)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_memory)
        self.timer.start(5000)

        self.update_memory()
    
    #Atualizar grafico barra
    def update_memory( self):
        
        total_memory = 0
        used_memory = 0
        free_memory = 0
        used_memory_percent = 0
        free_memory_percent = 0
        total_virtual_memory = 0

        try:
            with open("Global_information.txt","r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("Total Memory:"):
                        total_memory = float(line.split(": ")[1].split(" ")[0]) 
                    if line.startswith("Used Memory:"):
                        used_memory = float(line.split(": ")[1].split(" ")[0])
                    if line.startswith("Free Memory:"):
                        free_memory = float(line.split(": ")[1].split(" ")[0])
                    if line.startswith("Memory used percent:"):
                        used_memory_percent = float(line.split(": ")[1].strip()[:-1])
                    if line.startswith("Memory free percent:"):
                        free_memory_percent = float(line.split(": ")[1].strip()[:-1])
                    if line.startswith("Total Virtual Memory:"):
                        total_virtual_memory = float(line.split(": ")[1].split(" ")[0])
        except FileNotFoundError:
            pass


        memory_info_text = (f"Total Memory System : {used_memory} kB / {total_memory} kB \n"
                            f"Percentage of Memory Free: {free_memory_percent: .2f}% \n"
                            f"Percentage of Memory Used: {used_memory_percent: .2f}% \n"
                            f"Total RAM : {total_memory} kB \n"
                            f"Total Virtual Memory : {total_virtual_memory} kB"
                           )
        
        self.memory_info_label.setText(memory_info_text)


class ProcessListWidget(QFrame): #Classe para fazer a lista de processos

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout(self)
        self.mutex = threading.Lock() 

        self.process_count_label = QLabel("Process List count:")
        layout.addWidget(self.process_count_label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.counter = 0
        self.table.setHorizontalHeaderLabels(["Name of Process","User"])
        layout.addWidget(self.table)

        self.update_table_of_process()

    def update_table_of_process(self):
        self.table.setRowCount(0)

          #Essa parte é para ele fazer a tabela e a preencher os dados do txt 

        with self.mutex:  # Usa o mutex para proteger a leitura do arquivo
            with open("information_of_all_processes.txt","r") as file:
                lines = file.readlines()[1:]

                num_processes = len(lines)

                self.process_count_label.setText(f"process List Count: {num_processes}")
                for line in lines:
                    process_info = line.strip().split("  ", 1 )
                    if len(process_info) == 2 :
                        process_name, user_name = process_info
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        self.table.setItem(row_position, 0, QTableWidgetItem(process_name))
                        self.table.setItem(row_position, 1, QTableWidgetItem(user_name))


            self.table.resizeColumnsToContents()

            #Aqui é a configuração para fazer os tamanhos da tabela ficarem do tamanho certo
            for i in range(self.table.rowCount()):
                item = self.table.verticalHeaderItem(i)
                if item is None:
                    item = QTableWidgetItem()
                    item.setBackground(self.table.palette().color(self.table.backgroundRole()))
                    self.table.setVerticalHeaderItem(i, item)
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                for j in range(self.table.columnCount()):
                    item = self.table.item(i,j)
                    if item is None:
                        item = QTableWidgetItem()
                        item.setBackground(self.table.palette().color(self.table.backgroundRole()))
                        self.table.setItem(i, j, item)
                    item.setFlags(Qt.ItemFlag.NoItemFlags)

    def show_process_details(self, row, column):
        process_name = self.table.item(row,0).text()

 #classe para representar o quadrado aonde vai as informações do sistema
class FileSystemInfoWidget(QFrame):
    def __init__(self): #Metódo para iniciar o widget
        super().__init__()
        self.setStyleSheet("background-color:white")
        self.setup_ui()
        self.load_filesystem_info()

    def setup_ui(self): #método para carregar as configurações de layout
        layout = QVBoxLayout(self)

        self.filesystem_textedit = QTextEdit()
        self.filesystem_textedit.setReadOnly(True)
        self.filesystem_textedit.setMinimumHeight(200)
        self.filesystem_textedit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.filesystem_textedit)

    def load_filesystem_info(self): #Metodo que carrega o txt que tem as informações do sistema de arquivos
        try:
            with open("filesystem_information.txt", "r") as file:
                filesystem_info = file.read()
                self.filesystem_textedit.setPlainText(filesystem_info)
        except FileNotFoundError:
            QMessageBox.warning(self, "File not Found", "File 'filesystem_information.txt' not found.")                               
#classe que representa a parte de visualização usando o PyQt6


class DirectoryTreeViewWidget(QWidget): #classe que carrega o widget para mostrar a arvore de diretorios
    def __init__(self): #Metódo para inicar a widget
        super().__init__()
        self.setWindowTitle("Directory Tree View")
        self.setStyleSheet("background-color: white")
        self.setGeometry(100, 100, 600, 400)

        self.tree_widget = QTreeWidget() #função para criar no widget a arvore de diretórios
        self.tree_widget.setHeaderLabels(["Name", "Type"])
        self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Ajustar a largura da coluna
        self.tree_widget.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tree_widget.itemExpanded.connect(self.on_item_expanded)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)

        self.root_path = "/"  # Defina o diretório raiz aqui
        self.populate_tree(self.root_path)

    def populate_tree(self, root_path): #Metódo para para fazer expansão a partir da raiz 
        root_item = QTreeWidgetItem(self.tree_widget, [os.path.basename(root_path), "Directory"])
        root_item.setData(0, Qt.ItemDataRole.UserRole, root_path)  # Armazena o caminho completo como dado do item
        root_item.setExpanded(True)  # Expandir o item raiz por padrão
        self.tree_widget.addTopLevelItem(root_item)
        self.add_children(root_item, root_path)

    def add_children(self, parent_item, parent_path): #Metódo para adicionar as subpastas e subarquivos das pastas pai
        try:
            entries = os.listdir(parent_path)
            for entry in entries:
                full_path = os.path.join(parent_path, entry)
                item = QTreeWidgetItem([entry, self.get_item_type(full_path)])
                item.setData(0, Qt.ItemDataRole.UserRole, full_path)  # Armazena o caminho completo como dado do item
                if os.path.isdir(full_path):
                    item.addChild(QTreeWidgetItem())  # Adiciona um item dummy
                parent_item.addChild(item)
        except FileNotFoundError:
            print(f"Erro: Diretório não encontrado: {parent_path}")
        except PermissionError:
            print(f"Erro: Permissão negada ao acessar: {parent_path}")

    def get_item_type(self, path): #Metódo para que ele identifique se o item é uma pasta ou um arquivo
        if os.path.isdir(path):
            return "Directory"
        else:
            return "File"

    def on_item_expanded(self, item): #Metódo para substituir e mostrar as subpastas e arquivos dentro das pastas pai
        if item.childCount() == 1 and not item.child(0).text(0):
            item.takeChildren()  # Remove o item dummy
            path = item.data(0, Qt.ItemDataRole.UserRole)  # Obtém o caminho completo armazenado no item
            self.add_children(item, path)

class DirectoryContentsWidget(QFrame): #Classe para criar o widget aonde os conteúdos de um diretório selecionado vão aparecer no topo a direita
    def __init__(self): #Metódo para iniciar a classe e também criar a tabela com as 4 colunas que são de interesse
        super().__init__()
        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Size", "Permissions", "Type"])
        layout.addWidget(self.table)

    def list_directory_contents(self, directory_path): #Metódo que lista os conteúdos dos diretórios e coloca as informações obtidas na tabela do widget anterior
        self.table.setRowCount(0)
        try:
            entries = os.listdir(directory_path)
            for entry in entries:
                full_path = os.path.join(directory_path, entry)
                stat_info = os.stat(full_path)
                
                name = entry
                size = stat_info.st_size
                permissions = stat.filemode(stat_info.st_mode)
                file_type = "Directory" if os.path.isdir(full_path) else "File"
                
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(name))
                self.table.setItem(row_position, 1, QTableWidgetItem(str(size)))
                self.table.setItem(row_position, 2, QTableWidgetItem(permissions))
                self.table.setItem(row_position, 3, QTableWidgetItem(file_type))
                
            self.table.resizeColumnsToContents() #Ajusta o tamanho do conteúdo

        except Exception as e:
            print(f"Error listing directory contents: {e}")

#Classe que representa a view no modelo MVC e que seria a parte grafica         
class ViewofDashboard(QWidget):
    def __init__(self): #Metódo para inicar a dashboard com a definição gráfica geral de toda a dashboard
        super().__init__()
        self.setWindowTitle('Dashboard of Processes')
        self.setGeometry(100, 100, 1200, 600)  # Aumentei a largura para acomodar os novos widgets
        self.setStyleSheet("background-color: #D22525")

        main_layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.general_tab_layout = QVBoxLayout()
        self.directory_tab_layout = QVBoxLayout()  # Layout principal da aba de diretório

        self.tab_widget.addTab(QWidget(), "Geral")
        self.directory_tab = QWidget()
        self.tab_widget.addTab(self.directory_tab, "Diretório") #criação da aba diretório na dashboard

        self.setup_general_tab()
        self.setup_directory_tab()

        self.controller = Controller(self)
        self.controller.save_global_information_to_file("Global_information.txt")

    def setup_general_tab(self): #Método que cria a aba geral na dashboard e coloca as widgets correspondentes
        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.process_widget = ProcessListWidget()
        self.cpu_widget = CPUUsageWidget()
        self.memory_widget = MemoryUsageWidget()

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.process_widget, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.cpu_widget, 1, 0)
        self.grid_layout.addWidget(self.memory_widget, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.scroll_layout.addLayout(self.grid_layout)

        self.tab_widget.widget(0).setLayout(layout)
        self.process_widget.table.itemClicked.connect(self.on_process_item_clicked)

    def on_process_item_clicked(self, item): #Metódo que teoricamente seria para funcionar o clique no nome do processo
        row = item.row()
        process_name = self.process_widget.table.item(row, 0).text()
        user_name = self.process_widget.table.item(row, 1).text()
        pid = self.controller.get_pid_by_process_name(process_name, user_name)
        if pid:
            resources_info = self.controller.get_process_resources(pid)
            self.show_process_resources(process_name, resources_info)

    def setup_directory_tab(self): #Metódo para a criação da aba diretório na dashboard
        layout = QVBoxLayout(self.directory_tab)  # Layout principal da aba de diretório

        upper_layout = QHBoxLayout()  # Layout para os widgets na parte superior
        lower_layout = QGridLayout()  # Grid layout para os widgets na parte inferior

        self.filesystem_widget = FileSystemInfoWidget()
        self.directory_contents_widget = DirectoryContentsWidget()  # Adiciona o novo widget
        self.directory_widget = DirectoryTreeViewWidget()
        self.process_list_copy_widget = ProcessListWidget()  # Cópia do ProcessListWidget

        upper_layout.addWidget(self.filesystem_widget)
        upper_layout.addWidget(self.directory_contents_widget)

        lower_layout.addWidget(self.directory_widget, 0, 0)
        lower_layout.addWidget(self.process_list_copy_widget, 0, 1)

        layout.addLayout(upper_layout)
        layout.addLayout(lower_layout)

        self.directory_widget.tree_widget.itemClicked.connect(self.on_directory_item_clicked)  # Conectar o sinal de clique

        self.process_list_copy_widget.table.itemClicked.connect(self.on_process_item_clicked)  # Conectar o sinal de clique

    def on_directory_item_clicked(self, item): #Metódo tentativa para que funcione o clique em processo também na aba diretório na cópia do process list widget
        directory_path = item.data(0, Qt.ItemDataRole.UserRole)
        if os.path.isdir(directory_path):
            self.directory_contents_widget.list_directory_contents(directory_path)

    def show_process_resources(self, process_name, resources_info): #Tentativa de metódo 
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f"Resources for {process_name}")
        msg_box.setText(resources_info)
        msg_box.exec()

#classe que faz o controle para obter informações
class Controller:
    def __init__(self,view):
        self.view = view
        self.mutex = threading.Lock()  
        self.start_threads()

        self.get_filesystem_information()
    
    #classe que inicia as threads de obtenção de daddos e colocação
    def start_threads(self):
        threading.Thread(target=self.acquire_data, daemon=True).start()
        threading.Thread(target=self.put_results,  daemon=True).start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.put_results)
        self.timer.start(5000)

    #Metódo para conseguir recursos da lista de processos
    def get_process_resources(self, pid):
        resources_info = ""

        # Arquivos abertos
        resources_info += "Open Files:\n"
        try:
            fd_dir = f"/proc/{pid}/fd"
            for fd in os.listdir(fd_dir):
                fd_path = os.readlink(os.path.join(fd_dir, fd))
                resources_info += f"  FD {fd}: {fd_path}\n"
        except FileNotFoundError:
            resources_info += "  No open files or process not found.\n"
        except PermissionError:
            resources_info += "  Permission denied.\n"

        # Semáforos/mutexes
        resources_info += "\nSemaphores/Mutexes:\n"
        try:
            with open(f"/proc/{pid}/status", "r") as status_file:
                for line in status_file:
                    if line.startswith("Threads:"):
                        resources_info += f"  {line.strip()}\n"
                    if line.startswith("SigQ:"):
                        resources_info += f"  {line.strip()}\n"
        except FileNotFoundError:
            resources_info += "  Process not found.\n"
        except PermissionError:
            resources_info += "  Permission denied.\n"

        # Sockets
        resources_info += "\nSockets:\n"
        try:
            socket_dir = f"/proc/{pid}/fd"
            for fd in os.listdir(socket_dir):
                fd_path = os.readlink(os.path.join(socket_dir, fd))
                if "socket:" in fd_path:
                    resources_info += f"  {fd_path}\n"
        except FileNotFoundError:
            resources_info += "  No sockets or process not found.\n"
        except PermissionError:
            resources_info += "  Permission denied.\n"

        return resources_info

    #classe para pegar o usuario de quem o processo pertence
    def get_user_of_processes(self,proc_pid) :
        try:
            with open(f"/proc/{proc_pid}/status","r") as status_file:
                for line in status_file :
                    if line.startswith("Uid:"):
                        userid = int(line.split()[1])
                        break
                else:
                    userid = -1
        except FileNotFoundError :
            return "Unknown"
    
        if userid == 0 :
            return "root"
        else :
            try:
                with open("/etc/passwd","r") as passwd_file:
                    for line in passwd_file :
                        parts = line.split (":")
                        if int(parts[2]) == userid :
                            return parts[0]
            except FileNotFoundError:
                pass
            return "Basilio"
        
    #Classe para obter todos os processos que estão em execução
    def get_info_of_process(self):
        process = []
        for entry in os.scandir("/proc") :
            if entry.is_dir() and entry.name.isdigit() :
                pid = entry.name
                user = self.get_user_of_processes(pid)
                name = self.get_name_of_process(pid)
                process.append(ProcessInformation(pid,user,name))
        return process

    #classe para obter o nome do processo em execução
    def get_name_of_process(self,pid):
        try:
            with open(f"/proc/{pid}/comm","r") as comm_file:
                name = comm_file.readline().strip()
                if '/' in name:
                    name = name.split('/')[0]
            return name
        except FileNotFoundError:
            return "Unknown"

    #classe para pegar os dados periodicamente e atualizar o txt   
    def acquire_data(self):
        while True:
            processes_info = self.get_info_of_process()
            self.save_details_process_to_file(processes_info,"information_of_all_processes.txt")
            self.save_global_information_to_file("Global_information.txt")
            time.sleep(5)

    
    #classe para salvar os dados no sistema operacional
    def save_details_process_to_file(self, process_info, file_path):
        with self.mutex :
            with open(file_path,"w") as file:
                file.write("Processes:\n")
                for process_info in process_info:
                    process_name = process_info.name.ljust(30)
                    user_name = process_info.user.ljust(30)
                    file.write(f"{process_name}{user_name}\n")

    def get_pid_by_process_name(self, process_name, user_name):
        processes_info = self.get_info_of_process()
        for process in processes_info:
            if process.name == process_name and process.user == user_name:
                return process.pid
        return None
    
    #Atualiza a interface gráfica
    def put_results(self):

       self.view.process_widget.update_table_of_process()
       self.view.memory_widget.update_memory()

    #def para parar as threads que possam existir
    def stop_threads(self):
        self.stop_event.set()

    #def para ler a funçaõ das informações da memória a partir do /proc/meminfo
    def get_memory_information(self):
        with open('/proc/meminfo') as file:
            lines = file.readlines()

        memory_total = 0
        memory_free = 0
        memory_available = 0

        for line in lines:
            if line.startswith('MemTotal:'):
                memory_total = float(line.split()[1])
            elif line.startswith('MemFree:'):
                memory_free = float(line.split()[1])
            elif line.startswith('MemAvailable:'):
                memory_available= float(line.split()[1])
            elif line.startswith('SwapTotal:'):
                virtual_memory = float(line.split()[1])

        #Calcular a memória usada
        memory_used = memory_total - memory_free

        #Caclular a porcentagem da memória usada
        memoryused_percent = (memory_used / memory_total) * 100

        #Calcular a porcentagem de memória livre
        memoryfree_percent = 100 - memoryused_percent

        return memory_total, memory_free, memory_used, memoryused_percent, memoryfree_percent, virtual_memory
    
    #Função que salva os arquivos em texto
    def save_global_information_to_file(self, file_path):
        memory_total, memory_free, memory_used, memoryused_percent, memoryfree_percent, virtual_memory= self.get_memory_information()
        absoule_file_path = os.path.abspath(file_path)
        with open(absoule_file_path, "w") as file:
            file.write("Global Memory Information  \n")
            file.write("\n")
            file.write(f"Total Memory: {memory_total} kB \n")
            file.write(f"Free Memory: {memory_free} kB \n")
            file.write(f"Used Memory: {memory_used} kB \n")
            file.write(f"Memory free percent: {memoryfree_percent}% \n")
            file.write(f"Memory used percent: {memoryused_percent}% \n")
            file.write(f"Total Virtual Memory: {virtual_memory} kB \n")

    #Obter e criar informações de sistema de arquivos e guardar no txt
    def get_filesystem_information(self):
        filesytem_info_path = "filesystem_information.txt"
        with open(filesytem_info_path, "w") as file:
            with open('/proc/mounts', 'r') as f_mounts:
                for line in f_mounts:
                    fields = line.split()
                    if fields[0].startswith('/dev'):
                        device = fields[0]
                        mountpoint = fields[1]

                        statvfs = os.statvfs(mountpoint)
                        total_space = statvfs.f_frsize * statvfs.f_blocks
                        free_space = statvfs.f_frsize * statvfs.f_bfree
                        used_space = total_space - free_space
                        percent_used = (used_space / total_space) * 100

                        file.write(f"Partition: {device}\n")
                        file.write(f"Mountpoint: {mountpoint}\n")
                        file.write(f"Total Size: {total_space / (1024 * 1024)} MB\n")
                        file.write(f"Used: {used_space / (1024 * 1024)} MB\n")
                        file.write(f"Free: {free_space / (1024 * 1024)} MB\n")
                        file.write(f"Percent Used: {percent_used:.2f}% \n\n")

def main():
    app = QApplication([])
    controller = Controller
    window = DirectoryTreeViewWidget()
    view = ViewofDashboard()
    controller = Controller(view)
    controller.start_threads()
    window.show()
    view.show()
    app.exec()
    
if __name__ == "__main__":
    main()