# ./codespace/convert_pipeline.py
import os

last_gguf_file = ''

def quant_gguf():
    global last_gguf_file
    type_table = """
    2  or  Q4_0   :  3.56G, +0.2166 ppl @ LLaMA-v1-7B
    3  or  Q4_1   :  3.90G, +0.1585 ppl @ LLaMA-v1-7B
    8  or  Q5_0   :  4.33G, +0.0683 ppl @ LLaMA-v1-7B
    9  or  Q5_1   :  4.70G, +0.0349 ppl @ LLaMA-v1-7B
   10  or  Q2_K   :  2.63G, +0.6717 ppl @ LLaMA-v1-7B
   12  or  Q3_K   :  alias for Q3_K_M
   11  or  Q3_K_S :  2.75G, +0.5551 ppl @ LLaMA-v1-7B
   12  or  Q3_K_M :  3.07G, +0.2496 ppl @ LLaMA-v1-7B
   13  or  Q3_K_L :  3.35G, +0.1764 ppl @ LLaMA-v1-7B
   15  or  Q4_K   :  alias for Q4_K_M
   14  or  Q4_K_S :  3.59G, +0.0992 ppl @ LLaMA-v1-7B
   15  or  Q4_K_M :  3.80G, +0.0532 ppl @ LLaMA-v1-7B
   17  or  Q5_K   :  alias for Q5_K_M
   16  or  Q5_K_S :  4.33G, +0.0400 ppl @ LLaMA-v1-7B
   17  or  Q5_K_M :  4.45G, +0.0122 ppl @ LLaMA-v1-7B
   18  or  Q6_K   :  5.15G, -0.0008 ppl @ LLaMA-v1-7B
    7  or  Q8_0   :  6.70G, +0.0004 ppl @ LLaMA-v1-7B
    1  or  F16    :  13.00G              @ 7B
    0  or  F32    :  26.00G              @ 7B
    """
    
   
    # Define the argument names
    arg_names = ['gguf_file', 'quant_type', 'output_file']
    
    # Initialize a dictionary to store user inputs
    args = {}
    if last_gguf_file!="":
        args['gguf_file'] = input(f"gguf_file : (default: {last_gguf_file}): ") 
        if args['gguf_file']=="":
            args['gguf_file']=last_gguf_file

    else:
        args['gguf_file'] = input(f"gguf_file: ")


    # Check if the provided input files exist
    if not os.path.exists(args['gguf_file']):
        print(f"Error: The file '{args['gguf_file']}' does not exist.")
        return
    
    last_gguf_file = args['gguf_file']

    print("")
    # Display the type table
    print("Available Types:")
    print(type_table)
 
    args['quant_type'] = input(f"quant_type: ")

    quant_type = args['quant_type']
    # Map quant_type to the corresponding type abbreviation
    type_mapping = {
    '2': 'Q4_0',
    '3': 'Q4_1',
    '8': 'Q5_0',
    '9': 'Q5_1',
    '10': 'Q2_K',
    '11': 'Q3_K_S',
    '12': 'Q3_K_M',
    '13': 'Q3_K_L',
    '14': 'Q4_K_S',
    '15': 'Q4_K_M',
    '16': 'Q5_K_S',
    '17': 'Q5_K_M',
    '18': 'Q6_K',
    '7': 'Q8_0',
    '1': 'F16',
    '0': 'F32',
    }     
    # Get the corresponding abbreviation or use the original quant_type
    quantstring = type_mapping.get(quant_type, quant_type)
    basefile =  os.path.splitext(args['gguf_file'])[0]
    basefile = basefile.replace('-f16', '')
    # Update the output_file with the appropriate quant type
    new_out_file = basefile + f'_{quantstring}.gguf'

    args['output_file'] = input(f"output_file : (default: {new_out_file}): ")

    if args['output_file']=="":
        args['output_file']=new_out_file
                    
    # Check if the provided output file already exists
    if os.path.exists(args['output_file']):
        print(f"Error: The file '{args['output_file']}' already exists.")
        overwrite = input("Overwrite the file? (y/n): ")
        if overwrite == "y":
            os.remove(args['output_file'])
        else:
            args['output_file'] = input(f"output_file: ")
       

    # Call the external executable
    cmd = f"quantize.exe {args['gguf_file']} {args['output_file']} {args['quant_type']}"
    os.system(cmd)
    print(f"Quantization finished for {quantstring}")

#def quant_gguf():
#    arg_list_quant = ['gguf_file', 'output_file', 'quant type']
#    iter = -1
#    for arg in arg_list_quant:
#        iter = iter + 1
#        arg_list_quant[iter] = input(f"{arg}: ")
#
#    os.system(f"quantize.exe {arg_list_quant[0]} {arg_list_quant[1]} {arg_list_quant[2]}")

def hf_to_gguf():
    arg_list_hf = ['hf_dir']
    iter = -1
    for arg in arg_list_hf:
        iter = iter + 1
        arg_list_hf[iter] = input(f"{arg}: ")

    dir_model = arg_list_hf[0]

    #if not dir_model.is_dir():
    #    print(f'Error: {dir_model} is not a directory')
    #    return

    _, last_subfolder = os.path.split(dir_model)
    last_subfolder = last_subfolder.replace("_HF", "")
    last_subfolder = last_subfolder.replace(":", "")
    if len(last_subfolder) < 3:
        last_subfolder = 'llama-model'

    fname_out = os.path.join(dir_model, f'{last_subfolder}-f16.gguf')

    os.system(f"py convert.py {arg_list_hf[0]} --outtype f16 --outfile {fname_out}")

def hf_to_gguf4():
    arg_list_hf = ['hf_dir']
    iter = -1
    for arg in arg_list_hf:
        iter = iter + 1
        arg_list_hf[iter] = input(f"{arg}: ")

    dir_model = arg_list_hf[0]

    #if not dir_model.is_dir():
    #    print(f'Error: {dir_model} is not a directory')
    #    return

    _, last_subfolder = os.path.split(dir_model)
    last_subfolder = last_subfolder.replace("_HF", "")
    last_subfolder = last_subfolder.replace(":", "")
    if len(last_subfolder) < 3:
        last_subfolder = 'llama-model'

    fname_out = os.path.join(dir_model, f'{last_subfolder}-q8_0.gguf')

    os.system(f"py convert.py {arg_list_hf[0]} --outtype q8_0 --outfile {fname_out}")


def ggml_to_gguf():
    arg_list_ggml = ['ggml_file', 'output_file', 'metadata-dir']
    iter = -1
    for arg in arg_list_ggml:
        iter = iter + 1
        arg_list_ggml[iter] = input(f"{arg}: ")
    os.system(f"py convert-llama-ggml-to-gguf.py --input {arg_list_ggml[0]} --output {arg_list_ggml[1]} --model-metadata-dir {arg_list_ggml[2]}")

while True:
    print('#cherry-py\n')
    print("'1': hf-to-gguf")
    print("'2': ggml-to-gguf")
    print("'3': quantize-gguf")
    print("'4': Extra: hf to 8-bit gguf")
    print("'0': quit")
    convert_type = input(">>> ")
    if convert_type == "1":
        hf_to_gguf()
    elif convert_type == "2":
        ggml_to_gguf()
    elif convert_type == "3":
        quant_gguf()
    elif convert_type == "4":
        hf_to_gguf4()        
    elif convert_type == "0":
        print("Exiting the program.")
        break
