import json
import os

NULL_TOKEN = "Ø"
TRAININGFILE_DIR = "demo_corpus.jsonl"
ANNOTATED_DIR = "annotated.jsonl"
DICTCOLLECTION_DIR = "dicts_collection.jsonl"


def main():


  def annotator():
    while True:
      segmented_str = input("Enter segmented zh-Hant (tokens separated by space, e.g. 我 去 學校): ")
      token = segmented_str.split()
      if token:
       break

    while True:
      predicate_str = input("Enter predicate: ")
      if predicate_str.strip():
        break

    agent_str = input("Enter agent: ")
    if not agent_str.strip():
      agent_str = NULL_TOKEN

    theme_str = input("Enter theme: ")
    if not theme_str.strip():
      theme_str = NULL_TOKEN

    optional_role_str = input("Enter optional roles: ")
    split_optional_role_str = optional_role_str.split()

    optional_feature_str = input("Enter optional features: ")
    split_optional_feature_str = optional_feature_str.split()

    internal_dict = {
    "source": {
      "segmented": token,
      "raw": "".join(token)
      },
    "annotation": {
      "predicate": predicate_str,
      "roles": {
        "agent": agent_str,
        "theme": theme_str
      },
    "features": {
        }
      }
    }

    
    for i in split_optional_role_str:
      if i.count("=") == 1:
        x = i.split("=")
        y = x[0].strip()
        z = x[1].strip()
        if y and z:
          internal_dict["annotation"]["roles"][y] = z

    for i in split_optional_feature_str:
      if i.count("=") == 1:
        x = i.split("=")
        y = x[0].strip()
        z = x[1].strip()
        if y and z:
          internal_dict["annotation"]["features"][y] = z
    
    return internal_dict


  def sharegpt_export():

    annotated_line_count = -1
    if os.path.exists(ANNOTATED_DIR): 
      print("exist")

      with open(ANNOTATED_DIR, "r", encoding="utf-8") as g:
        for annotated_line_count, element in enumerate(g):
          pass
        print(annotated_line_count)

    with open(TRAININGFILE_DIR, "r", encoding="utf-8") as f:
        for training_line_count, element in enumerate(f):
          if  training_line_count <= annotated_line_count:
            continue
          y = json.loads(element)
          print(y)

          while True:
            annotation_ctrl = input("DO you want to annotate? (y/n/q)")

            if annotation_ctrl.strip() == "y" or annotation_ctrl.strip() == "Y":
                
                with open(ANNOTATED_DIR, "a", encoding="utf-8") as g:
                
                    with open(DICTCOLLECTION_DIR, "a", encoding="utf-8") as h: 
                        a = annotator()
                        b = a["annotation"]
                        y["messages"][1]["content"] = y["messages"][1]["content"] + f"\n<annotation>{b}</annotation>"
                        z = json.dumps(y, ensure_ascii=False)
                        g.write(z + "\n")
                        json_object = json.dumps(a, ensure_ascii=False, indent=2)
                        h.write(json_object + "\n")
                        break
                

            elif annotation_ctrl.strip() == "n" or annotation_ctrl.strip() == "N":
                with open(ANNOTATED_DIR, "a", encoding="utf-8") as g:
                    z = json.dumps(y, ensure_ascii=False)
                    g.write(z + "\n")
                    break
            
            elif annotation_ctrl.strip() == "q" or annotation_ctrl.strip() == "Q":
              print("Session terminated")
              return 

        print("Session completed")
        

  sharegpt_export()

if __name__ == "__main__":
  main()
