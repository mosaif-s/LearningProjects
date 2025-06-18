import streamlit as st
from streamlit import file_uploader, spinner

from main import load_document, chunk_data, calculate_embedding_costs, insert_or_fetch_embeddings, \
    delete_pinecone_index, ask_and_get_answer

def clear_history():
    if "history" in st.session_state:
        del st.session_state['history']

if __name__=="__main__":
    import os
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

    st.image('img_1.png')
    st.subheader("LLM Private Documents QandA Application")
    with st.sidebar:
        api_key=st.text_input("OpenAI API Key:", type='password')
        if api_key:
            os.environ['OPENAI_API_KEY']=api_key
        uploaded_file=file_uploader("Upload a file:", type=['pdf','txt','docx'])
        chunks_size=st.number_input('Chunk size:', min_value=100, max_value=2848,value=512, on_change=clear_history)
        k=st.number_input('k',min_value=1,max_value=20,value=3, on_change=clear_history)
        add_data=st.button("Add data", on_click=clear_history)

        if uploaded_file and add_data:
            with st.spinner("Reading, chunking and embedding your file..."):
                bytes_data=uploaded_file.read()
                file_name=os.path.join('./', uploaded_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)

                data=load_document(file_name)
                chunks = chunk_data(data, chunk_size=chunks_size)
                st.write(f"Chunk size: {chunks_size}, Chunks: {len(chunks)}")
                tokens, embcost=calculate_embedding_costs(chunks)
                st.write(f"Embedding cost: ${embcost:.4f}")
                delete_pinecone_index() #remove if using same document again and again
                index_name = 'askadocument'
                vector_store = insert_or_fetch_embeddings(index_name, chunks)
                st.session_state.vs=vector_store #why do this, just ude vector_store as variable no?
                st.success('File uploaded and embedded successfully!')

    q=st.text_input("Ask a question about your document")
    if q:
        if 'vs' in st.session_state:
            vector_store=st.session_state.vs
            answer=ask_and_get_answer(vector_store,q,k)
            #st.text_area('LLM Answer:', value=answer)
            import time
            placeholder = st.empty()
            display = ""
            for char in answer:
                display += char
                placeholder.text_area("Assistant's Response", value=display, disabled=False, height=400)
                time.sleep(0.01)

            st.divider()
            if 'history' not in st.session_state:
                st.session_state.history=''

            value=f"Q:{q}\n A:{answer}"
            dashes="-"*100
            st.session_state.history=f"{value} \n {dashes}\n {st.session_state.history}"
            h=st.session_state.history
            st.text_area(label='Chat History', value=h, key='history', height=400, disabled=True)