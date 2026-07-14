import os
import json

class Agent:
    def __init__(self):
        self.setup_tools()
        self.messages= [
            {"role": "system", "content": "Eres un asistente útil que habla español y eres conciso con tus respuestas"},
        ]        
    def setup_tools(self):
        self.tools =[
            {
                "type": "function",
                "name": "list_files_in_dir",
                "description": "Lista todos los archivos en un directorio especificado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "El directorio del cual listar los archivos. Por defecto es el directorio actual."
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "read_file",
                "description": "Lee el contenido de un archivo especificado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "La ruta del archivo a leer."
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "type": "function",
                "name": "edit_file",
                "description": "Edita un archivo especificado reemplazando un contenido previo con un nuevo contenido.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "La ruta del archivo a editar."
                        },
                        "prev_content": {
                            "type": "string",
                            "description": "El contenido previo que se desea reemplazar."
                        },
                        "new_content": {
                            "type": "string",
                            "description": "El nuevo contenido que reemplazará al contenido previo."
                        }
                    },
                    "required": ["file_path", "new_content"]
                }
            }
        ]
    
    def list_files_in_dir(self,directory="."):
        print("Herramienta llamada: list_files_in_dir")
        try:
            files = os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {f"Error":"Error al listar archivos en el directorio '{directory}': {e}"}
        
  
    #Herramienta: Leer archivos
    def read_file(self, file_path):
        print(f"Herramienta llamada: read_file")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error al leer el archivo '{file_path}': {e}"
    #Herramienta: Editar archivos
    def edit_file(self, file_path, prev_content, new_content):
        print(f"Herramienta llamada: edit_file")
        try:
            existed=os.path.exists(file_path)
            if existed and prev_content:
                content = self.read_file(file_path)
                if prev_content not in content:
                    return f"Texto {prev_content} no encontrado en el archivo."
                content= content.replace(prev_content, new_content)
            else:
                dir_name = os.path.dirname(file_path)
                if dir_name and not os.path.exists(dir_name):
                    os.makedirs(dir_name,exist_ok=True)
                content=new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content) 
            action = "actualizado" if existed and prev_content else "creado"
            return f"Archivo {file_path} {action}  con éxito."
        except Exception as e:
            return f"Error al editar el archivo '{file_path}': {e}"
        
    def process_response(self,response):
        #Trye = si llama a una herramienta, ejecutarla y devolver la respuesta, False = si no llama a una herramienta, devolver la respuesta del asistente
        self.messages+= response.output
        for output in response.output:
            if output.type=="function_call":
                fn_name= output.name
                args=json.loads(output.arguments)
                print(f"El asistente ha llamado a la herramienta '{fn_name}'")
                print(f"Argumentos: {args}")
                if fn_name=="list_files_in_dir":
                    result= self.list_files_in_dir(**args)
                elif fn_name=="read_file":
                    result= self.read_file(**args)
                elif fn_name=="edit_file":
                    result= self.edit_file(**args)

                #print(f"Resultado de la herramienta: {result}")
                self.messages.append({
                    "type": "function_call_output","call_id": output.call_id,
                    "output": json.dumps(result)
                    })
                return True
            elif output.type=="message":
                reply= "\n".join([msg.text for msg in output.content])
                print(f"Asistente: {reply}")
        return False  