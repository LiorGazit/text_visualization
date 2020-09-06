# @article {kessler2017scattertext,
#  author = {Kessler, Jason S.},
#             title = {Scattertext: a Browser - Based Tool
#             for Visualizing how Corpora Differ},
#             booktitle = {Proceedings of ACL-2017 System Demonstrations},
#             year      = {2017},
#             address   = {Vancouver, Canada},
#             publisher = {Association for Computational Linguistics},
#             }

#!pip install scattertext
import scattertext as st
import pandas as pd
import regex as re
import os


def scattertext(df,
                category_column,
                positive_category,
                positive_category_pretty_name,
                negative_category_pretty_name,
                parsed_column,
                neutral_category,
                html_file_name,
                remove_stop_words):
    """
    This function applies Jason Kessler's scattertext visualization in HTML.
    See here: https://github.com/JasonKessler/scattertext

    :param df: Dataframe of the data set
    :param category_column: Name of the column in df that the data is to be split by.
            Typically the labels column in a binary classification problem.
    :param positive_category: Which of the categories in category_column is to be considered positive
    :param positive_category_pretty_name: How to print out the value of positive_category
    :param negative_category_pretty_name: How to print out the value of the negative category
    :param parsed_column: The column name for the text data
    :param neutral_category: The column name for another column that may be used for exploration
    :param html_file_name: File name to save to
    :param remove_stop_words: Boolean, whether to remove stopwords
    :return: No value returned.
    """

    if remove_stop_words:
        corpus = st.CorpusFromParsedDocuments(
            df, category_col=category_column, parsed_col=parsed_column
        ).build().get_stoplisted_unigram_corpus().compact(st.AssociationCompactor(2000))
    else:
        corpus = st.CorpusFromParsedDocuments(
            df, category_col=category_column, parsed_col=parsed_column
        ).build().get_unigram_corpus().compact(st.AssociationCompactor(2000))

    html = st.produce_scattertext_explorer(
        corpus,
        category=positive_category, category_name=positive_category_pretty_name, not_category_name=negative_category_pretty_name,
        minimum_term_frequency=0, pmi_threshold_coefficient=0,
        width_in_pixels=1000, metadata=corpus.get_df()[neutral_category],
        transform=st.Scalers.dense_rank
    )
    open(html_file_name, 'w').write(html)


if __name__ == "__main__":
    html_file_name = 'demo_compact.html'
    url_for_data_file = 'https://datasets.appen.com/appen_datasets/Medical-Relation-Extraction/train.csv'
    data_file = "Medical Information Extraction Pubmed train.csv"
    remove_stop_words = True

    # Data taken from: https://appen.com/datasets/medical-sentence-summary-and-relation-extraction/
    # Check whether data file exists, if not, download it:
    does_data_file_exist = os.path.exists(data_file)
    if does_data_file_exist == False:
        # Download file:
        print("Downloading the data file from:   " + url_for_data_file)
        df_raw = pd.read_csv(url_for_data_file)
        df_raw.to_csv(data_file)
    else:
        df_raw = pd.read_csv(data_file)

    # Make a binary column to tell whether pain is present in the diagnoses:
    df_binary = df_raw
    df_binary["binary"] = [str('pain' in (sentence[0] + sentence[1]).lower()) for sentence in df_raw[["term1", "term2"]].values]

    # Making a column of the year out of the "_created_at" which has the format "'7/13/2014 13:48:35'":
    df_binary["year"] = [re.split('/| ', date_string)[2] for date_string in df_binary["_created_at"]]

    # Keep only necessary columns and drop duplicates:
    df_processed = df_binary[["sentence", "binary", "year"]].drop_duplicates(keep="first", inplace=False, ignore_index=True)

    df = df_processed.assign(
        parse=lambda df: df.sentence.apply(st.whitespace_nlp_with_sentences)
    )
    
    category_column = 'binary'
    positive_category = 'True'
    positive_category_pretty_name = 'Pain_Diagnosed'
    negative_category_pretty_name = 'No_Pain_Diagnosed'
    parsed_column = 'parse'
    neutral_category = 'year'

    scattertext(df,
                category_column,
                positive_category,
                positive_category_pretty_name,
                negative_category_pretty_name,
                parsed_column,
                neutral_category,
                html_file_name,
                remove_stop_words)
