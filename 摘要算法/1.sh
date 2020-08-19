mkdir -p mono
for SPLIT in train valid test; do
    python encode.py \
        --inputs wikitext-103-raw/wiki.${SPLIT}.raw \
        --outputs mono/${SPLIT}.txt \
        --workers 60; \
done