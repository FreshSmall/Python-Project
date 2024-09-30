from openai import OpenAI

client = OpenAI(
    api_key="gAAAAABmFmLplODi2NxnZYnkqEG177I6cfZguGJ_kYncc6y95ViTka9uMryxXla1KJWSRtp2Lv7-p5Gk-rCxMvALTUneEykefaUIkhPeD_uDam3ENi2OMoKn3ui5FWMIeHcbUXfbQ_Yl",
    base_url="https://aiops-api.baijia.com/openai/v1"
)


def kotlin_to_java(input):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "把Kotlin 代码转换成 Java 代码。要输出完整的java代码"},
            {"role": "user", "content": f"{input}"}
        ]
    )
    return completion.choices[0].message.content


if __name__ == '__main__':
    input = '''
    package com.baijia.tmk.service.mark

import com.baijia.tmk.common.enums.FieldTypeEnum
import com.baijia.tmk.service.entity.CommonMarkRecordEntity
import com.baijia.tmk.service.entity.FormStyleEntity
import com.baijia.tmk.service.entity.MarkFieldEntity
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.COLLECTION_NAME
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.DATA_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.MARK_ID_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.SCENE_ID_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.TASK_ID_FIELD
import com.baijia.tmk.service.service.MarkFieldService
import com.baijia.tmk.service.service.SceneService
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.data.mongodb.core.query.Criteria
import org.springframework.data.mongodb.core.query.Query
import org.springframework.data.mongodb.core.query.Update
import org.springframework.stereotype.Service
import java.math.BigDecimal
import java.math.RoundingMode

@Service
class MarkDynamicService(val mongoTemplate: MongoTemplate,
    val markFieldService: MarkFieldService, val sceneService: SceneService) {


    fun findByMarkId(markId: Long): Map<String, Any> {
        val query = Query.query(Criteria.where(MARK_ID_FIELD).`is`(markId))
        val dynamicMark = mongoTemplate.findOne(query, MarkDynamicEntity::class.java)
        return dynamicMark?.data ?: mutableMapOf()
    }

    fun findByTaskId(taskId: Long): List<MarkDynamicEntity> {
        val query = Query.query(Criteria.where(TASK_ID_FIELD).`is`(taskId))
        return mongoTemplate.find(query, MarkDynamicEntity::class.java) ?: listOf()
    }

    fun findByTaskIds(taskId: List<Long>): Map<Long, List<MarkDynamicEntity>> {
        val query = Query.query(Criteria.where(TASK_ID_FIELD).`in`(taskId))
        return mongoTemplate.find(query, MarkDynamicEntity::class.java)?.groupBy { it.taskId }
            ?: emptyMap()
    }

    fun findMapByTaskId(taskId: Long): Map<Long, Map<String, Any>> {
        val dynamicMarks = findByTaskId(taskId)
        return dynamicMarks.associate { it.markId to it.data }
    }

    fun insertMark(mark: CommonMarkRecordEntity,
        externalData: Map<String, Any>,
        formStyle: FormStyleEntity) {
        if (externalData.isEmpty()) {
            return
        }
        val sceneId = mark.sceneId ?: return
        val markFieldList = markFieldService.listMarkFieldsByFormId(formStyle.formStyleId, sceneId)
        if (markFieldList.isEmpty()) {
            return
        }
        val dynamicMark = MarkDynamicEntity().apply {
            this.markId = mark.id
            this.taskId = mark.taskId
            this.sceneId = sceneId
            this.formId = formStyle.formStyleId ?: ""
            this.formInstanceId = mark.formInstanceId ?: ""
        }
        val markData = mutableMapOf<String, Any>()
        for (field in markFieldList) {
            val s = externalData[field.fieldName] ?: continue
            markData[field.fieldName] = s
        }
        dynamicMark.data = markData
        mongoTemplate.insert(dynamicMark)
    }

    fun updateMark(mark: CommonMarkRecordEntity,
        taskId: Long,
        sceneId: String,
        externalData: Map<String, Any>) {
        if (externalData.isEmpty()) {
            return
        }
        val markFieldList = markFieldService.listMarkFieldsByFormId(mark.formStyleId, sceneId)
        if (markFieldList.isEmpty()) {
            return
        }
        val query =
            Query.query(Criteria.where(TASK_ID_FIELD).`is`(taskId).and(MARK_ID_FIELD).`is`(mark.id)
                .and(SCENE_ID_FIELD).`is`(sceneId))
        val dynamicMark =
            mongoTemplate.findOne<MarkDynamicEntity>(query, MarkDynamicEntity::class.java) ?: return
        val markData = mutableMapOf<String, Any>()
        for (field in markFieldList) {
            val s = externalData[field.fieldName] ?: continue
            markData[field.fieldName] = s
        }
        dynamicMark.data = markData
        val update = Update().set(DATA_FIELD, externalData)
        mongoTemplate.updateMulti(query, update, COLLECTION_NAME)
    }

    fun handleFieldData(s: Any, fieldEntity: MarkFieldEntity): Any {
        return when (fieldEntity.fieldType) {
            FieldTypeEnum.STRING.code -> s.toString()
            FieldTypeEnum.TEXT.code -> s.toString()
            FieldTypeEnum.DATE.code -> s
            FieldTypeEnum.BUSINESS_ENUM.code -> Integer.parseInt(s.toString())
            FieldTypeEnum.NUMBER.code -> BigDecimal(s.toString()).setScale(2, RoundingMode.HALF_UP)
            else -> s
        }
    }
}
    '''
    print(kotlin_to_java(input))
