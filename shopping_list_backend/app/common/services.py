from typing import Any, Optional

from app.common.types import DjangoModel


def update_instance(
    *, instance: DjangoModel, data: dict[str, Any], fields: Optional[tuple[str, ...]] = None
) -> tuple[DjangoModel, bool]:
    is_updated = False

    if fields is None:
        fields = iter(data)

    for field in fields:
        if field not in data or not hasattr(instance, field) or getattr(instance, field) == data[field]:
            continue
        is_updated = True
        setattr(instance, field, data[field])

    if is_updated:
        instance.save()

    return instance, is_updated


def update_instances(*, instances: dict[DjangoModel, tuple[str, ...]], data: dict[str, Any]) -> dict[DjangoModel, bool]:
    updated_instances = {instance: False for instance in instances}
    updated_instances_data = {instance: {} for instance in instances}
    field_to_instance_mapping = {field: instance for instance, fields in instances.items() for field in fields}

    for field, value in data.items():
        instance = field_to_instance_mapping[field]
        updated_instances_data[instance][field] = value

    for instance, data in updated_instances_data.items():
        updated_instance, is_updated = update_instance(instance=instance, data=data)
        updated_instances[updated_instance] = is_updated

    return updated_instances
