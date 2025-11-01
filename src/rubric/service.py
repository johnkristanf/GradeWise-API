from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select
from src.rubric.schemas import LLMConsumableRubricOut
from src.rubric.models import (
    Criterion,
    CriterionLevelDescriptor,
    PerformanceLevel,
    Rubric,
)


class RubricService:
    async def create_rubric(self, rubric_data: dict, session: AsyncSession):
        rubric = Rubric(
            name=rubric_data["name"],
            student_level=rubric_data["student_level"],
            grade_intensity=rubric_data["grade_intensity"],
            language=rubric_data["language"],
            essay_type=rubric_data["essay_type"],
        )

        session.add(rubric)
        await session.flush()

        # 2. Create and insert Criteria
        criteria_map = {}  # Map old IDs to new database IDs
        for criterion in rubric_data["criteria"]:
            db_criterion = Criterion(title=criterion["name"], rubric_id=rubric.id)
            session.add(db_criterion)
            await session.flush()
            criteria_map[criterion["id"]] = db_criterion.id

        # 3. Create and insert Performance Levels
        levels_map = {}  # Map old IDs to new database IDs
        for level in rubric_data["performance_levels"]:
            db_level = PerformanceLevel(
                label=level["label"], score=level["score"], rubric_id=rubric.id
            )
            session.add(db_level)
            await session.flush()
            levels_map[level["id"]] = db_level.id

        # 4. Create and insert Descriptors
        descriptors = rubric_data["descriptors"]
        for criterion_old_id, level_descriptors in descriptors.items():
            for level_old_id, descriptor_text in level_descriptors.items():
                db_descriptor = CriterionLevelDescriptor(
                    criterion_id=criteria_map[int(criterion_old_id)],
                    level_id=levels_map[int(level_old_id)],
                    descriptor=descriptor_text,
                )
                session.add(db_descriptor)

        # 5. Commit all changes
        await session.commit()
        await session.refresh(rubric)

        return rubric

    async def async_get_rubric_by_id(self, rubric_id, session: AsyncSession) -> Rubric | None:
        statement = (
            select(Rubric)
            .where(Rubric.id == rubric_id)
            .options(
                selectinload(Rubric.criterion)
                .selectinload(Criterion.descriptors)
                .selectinload(CriterionLevelDescriptor.performance_levels)
            )
        )

        result = await session.execute(statement)
        rubric_orm = result.scalars().first()
        if not rubric_orm:
            return None
        await session.refresh(rubric_orm)

        return LLMConsumableRubricOut.model_validate(rubric_orm)

    def sync_get_rubric_by_id(self, rubric_id, session: Session) -> Rubric | None:
        statement = (
            select(Rubric)
            .where(Rubric.id == rubric_id)
            .options(
                selectinload(Rubric.criterion)
                .selectinload(Criterion.descriptors)
                .selectinload(CriterionLevelDescriptor.performance_levels)
            )
        )

        result = session.execute(statement)
        rubric_orm = result.scalars().first()
        if not rubric_orm:
            return None
        session.commit()
        session.refresh(rubric_orm)

        return LLMConsumableRubricOut.model_validate(rubric_orm)
